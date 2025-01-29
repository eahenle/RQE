from ..Agent import Agent
from ...config import _DEFAULTS
import os
import sqlite3
from time import time

# defaults ## TODO: deal with this better
__MEM0_API_KEY_PATH__ = ".mem0"
__OPENAI_API_KEY_PATH__ = ".openai"
__DATABASE_PATH__ = "data/movie.sqlite"
__SYSTEM_PROMPT_FILES__ = {
    "select_tables" : "system/select_tables.txt",
    "create_sql_query" : "system/create_sql_query.txt"
}
__SCHEMA_TXT__ = "data/schema.txt" ## TODO: make this a random temporary file
__OPENAI_MODEL__ = "gpt-4o"

class IMDBot(Agent):
    def __init__(self, database_path=__DATABASE_PATH__, schema_txt=__SCHEMA_TXT__, openai_key_path=_DEFAULTS["OpenAI API key path"], model=_DEFAULTS["OpenAI model"], system_files=__SYSTEM_PROMPT_FILES__, mem0_key_path=_DEFAULTS["mem0 API key path"]): 
        super().__init__(openai_key_path=openai_key_path, model=model, mem0_key_path=mem0_key_path)
        # args/settings/params
        self.db_path = database_path
        self.schema_txt = schema_txt
        self.model = model
        self.system_files = system_files
        # setup
        self.db_conn = self.connect()
        self.db_schema = self.init_schema()
        return
    
    def query(self, user_query:str, retry_timeout:float=5) -> str:
        """Query the IMDB database using LLM-generated SQL."""
        starttime = time()
        while time() - starttime < retry_timeout:
            try:
                tables = self.select_tables(user_query)
                sql_query = self.create_sql_query(user_query, tables)
                sql_response = self.execute_sql(sql_query)
                output = self.format_output(user_query, sql_response)
                self.mem0.add(user_query, user_id=self.user_id)
                return output
            except Exception as e:
                print(e)

    def connect(self):
        """Connect to sqlite3 database at `db_path` only if file found."""
        if os.path.exists(self.db_path):
            return sqlite3.connect(self.db_path)
        else:
            raise FileNotFoundError(self.db_path)

    def execute_sql(self, query:str) -> list:
        """Connect to the database at the indicated path and execute a SQL query."""
        cursor = self.db_conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def init_schema(self) -> str:
        """
        Extract the table/column schema of a sqlite3 database to a text file.
        """
        cursor = self.db_conn.cursor()
        # read the table names from the DB metadata
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name;")
        tables = [x[0] for x in cursor.fetchall() if not x[0].startswith("sqlite_")]
        # build the schema up table by table
        schema = ""
        for table in tables:
            # get column names from table metadata
            cursor = self.db_conn.cursor()
            cursor.execute(f"SELECT name FROM pragma_table_info('{table}');")
            columns = [x[0] for x in cursor.fetchall()]
            # format list of columns
            col_str = ""
            for column in columns:
                col_str += column + ", "
            col_str = col_str[:-2]
            # format table scheme and append it to the schema string
            schema += f"\n{table};Table: {table}\\nColumns: \\n{col_str}"
        # trim leading newline
        schema = schema[1:]
        # write to file
        with open(self.schema_txt, "w") as f:
            f.write(schema)
        return schema

    def call_model(self, query:str, system_message:str="") -> str:
        """
        Run the query with optional `system_message` on the selected model.
        """
        return self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": query}
            ]
        ).choices[0].message

    def select_tables(self, user_query:str) -> list:
        """
        Use the LLM to choose tables from the database.
        """
        system_message = open(self.system_files["select_tables"], "r").read() ## TODO: move file reads to __init__
        tables = self.call_model(user_query, system_message).content.split(",")
        return tables ## TODO: if a table is not in the schema, do something

    def create_sql_query(self, user_query:str, tables:list):
        """
        Produce a SQL query based on the `user_query` and `schema_file`.
        The list of `tables` is used to confine the SQL's scope.
        """
        # parse tables metadata from schema
        schema = open(self.schema_txt,"r").readlines()
        tables_data = ""
        for scheme in schema:
            data = scheme.split(";")
            if data[0].strip() in tables:
                tables_data += data[1] + '\n'
        # generate the system prompt
        system_message = open(self.system_files["create_sql_query"], "r").read()
        system_message = system_message.replace("{tables}", tables_data)
        system_message = system_message.replace("{schema}", f"{schema}")
        # generate the SQL
        content = self.call_model(user_query, system_message).content
        # strip markdown
        content = content.replace("```sql", "").replace("```", "")
        return content
    
    def format_output(self, usr_query:str, raw_output:str) -> str:
        # usr_query argument could be useful for formatting via LLM
        return raw_output ## TODO: actually do something with formatting
