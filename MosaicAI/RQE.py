from Agent import Agent
from IMDBot import IMDBot
from defaults import _DEFAULTS

class RouterQueryEngine(Agent):
    def __init__(self, openai_key_path=_DEFAULTS["OpenAI API key path"], model=_DEFAULTS["OpenAI model"], mem0_key_path=_DEFAULTS["mem0 API key path"]):
        super().__init__(openai_key_path=openai_key_path, model=model, mem0_key_path=mem0_key_path)
        self.agents = {"imdbot": IMDBot(), "fallback": super()}
        self.system_message["classify_query"] = "Is this a movie-related query?"
        return
    
    def query(self, usr_query:str) -> str:
        """
        Route the query to the appropriate agent based on the query content.
        """
        # ask LLM to classify the query
        is_movie_query = super().query(usr_query, system_message=self.system_message["classify_query"]) == "Yes"
        # if about movies, ask IMDBot
        if is_movie_query:
            return self.agents["imdbot"].query(usr_query)
        # otherwise, ask fallback agent
        else:
            return self.agents["fallback"].query(usr_query)

if __name__ == "__main__":
    rqe = RouterQueryEngine()

    def test_query(query:str) -> None:
        print("## QUERY ##\n", query)
        print("## RESPONSE ##\n", rqe.query(query))
        # print("## MEMORY ##\n", rqe.mem0.search(query)) ## TODO: figure this out
        return

    # this query should be handled by IMDBot
    test_query("List the most popular movies from the years 2000-2006.")
    # this query should be handled by the fallback agent
    test_query("What is the capital of France?")
