from Agent import Agent
from defaults import _DEFAULTS

class RouterQueryEngine(Agent):
    def __init__(self, openai_key_path=_DEFAULTS["OpenAI API key path"], model=_DEFAULTS["OpenAI model"], mem0_key_path=_DEFAULTS["mem0 API key path"]):
        super().__init__(openai_key_path=openai_key_path, model=model, mem0_key_path=mem0_key_path)
        return

if __name__ == "__main__":
    rqe = RouterQueryEngine()
    query = "List the most popular movies from the years 2000-2006."
    print(rqe.query(query))
    print(rqe.mem0.search(query))
