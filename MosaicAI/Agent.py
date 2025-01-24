import os
from openai import OpenAI
from mem0 import MemoryClient
from defaults import _DEFAULTS

class Agent():
    def __init__(self, openai_key_path=_DEFAULTS["OpenAI API key path"], model=_DEFAULTS["OpenAI model"], mem0_key_path=_DEFAULTS["mem0 API key path"]): 
        # args/settings/params
        self.model = model
        # setup
        if os.path.exists(openai_key_path):
            # read key from local file and connect to the OpenAI API
            self.openai = OpenAI(api_key=open(openai_key_path).read().strip())
        else:
            self.openai = OpenAI() # backup option: read env vars
        self.mem0 = MemoryClient(api_key=open(mem0_key_path).read().strip())
        self.user_id = 42 ## TODO
        return

    def query(self, usr_query:str, system_message:str="") -> str:
        """
        Run the query with optional `system_message` on the selected model.
        """
        return self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": usr_query}
            ]
        ).choices[0].message
