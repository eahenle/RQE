import os
from openai import OpenAI
from mem0 import MemoryClient
from defaults import _DEFAULTS

class Agent():
    """
    Agent is the super-class to all AI agents in the MosaicAI system.
    It provides a common interface for all agents to interact with the OpenAI API and the mem0 API.
    """
    def __init__(self, openai_key_path=_DEFAULTS["OpenAI API key path"], model=_DEFAULTS["OpenAI model"], mem0_key_path=_DEFAULTS["mem0 API key path"]): 
        # args/settings/params
        self.model = model
        self.system_message = {}
        self.agents = {}
        # setup
        if os.path.exists(openai_key_path):
            # read key from local file and connect to the OpenAI API
            self.openai = OpenAI(api_key=open(openai_key_path).read().strip())
        else:
            self.openai = OpenAI() # backup option: read env vars
        if os.path.exists(mem0_key_path):
            # read key from local file and connect to the mem0 API
            self.mem0 = MemoryClient(api_key=open(mem0_key_path).read().strip())
        else:
            print("Error: mem0 API key not found.")
            exit(1)
        self.user_id = 42 ## TODO
        return

    def query(self, usr_query:str, system_message:str="") -> str:
        """
        Run the query with optional `system_message` on the selected model.
        """
        if len(system_message) == 0:
            system_message = ""
        return self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role" : "system", "content" : system_message},
                {"role" : "user", "content" : usr_query}
            ]
        ).choices[0].message.content
