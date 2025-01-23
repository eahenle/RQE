import os
import sqlite3

from openai import OpenAI
from mem0 import MemoryClient

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

class Querybot():
    def __init__(self, database_path=__DATABASE_PATH__, schema_txt=__SCHEMA_TXT__, openai_key_path=__OPENAI_API_KEY_PATH__, model=__OPENAI_MODEL__, system_files=__SYSTEM_PROMPT_FILES__, mem0_key_path=__MEM0_API_KEY_PATH__): 
        # args/settings/params
        self.db_path = database_path
        self.schema_txt = schema_txt
        self.model = model
        self.system_files = system_files
        # setup
        self.db_conn = self.connect()
        self.db_schema = self.init_schema()
        if os.path.exists(openai_key_path):
            # read key from local file and connect to the OpenAI API
            self.openai = OpenAI(api_key=open(openai_key_path).read())
        else:
            self.openai = OpenAI() # backup option: read env vars
        self.mem0 = MemoryClient(api_key=open(mem0_key_path).read())
        self.user_id = 42 ## TODO
        return
    
    def query(self, user_query:str) -> str:
        """Query the IMDB database using LLM-generated SQL."""
        self.mem0.add(user_query, user_id=self.user_id)
        return self.format_output(
            user_query, 
            self.execute_sql(
                self.create_sql_query(
                    user_query, 
                    self.select_tables(user_query)
                )
            )
        )

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
        tables_data = ""
        for scheme in open(self.schema_txt,"r").readlines():
            data = scheme.split(";")
            if data[0].strip() in tables:
                tables_data += data[1] + '\n'
        # generate the system prompt
        system_message = open(self.system_files["create_sql_query"], "r").read()
        system_message = system_message.replace("{tables}", tables_data)
        # generate the SQL
        content = self.call_model(user_query, system_message).content
        # strip markdown
        content = content.replace("```sql", "").replace("```", "")
        return content
    
    def format_output(self, raw_output:str) -> str:
        return raw_output ## TODO: actually do something with formatting


if __name__ == "__main__":
    bot = Querybot()
    query = "List the most popular movies from the years 2000-2006."
    print(bot.query(query))
    print(bot.mem0.search(query))
