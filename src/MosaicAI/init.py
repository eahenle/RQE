def launch():
    from src.MosaicAI.util import FrontEnd
    FrontEnd().run()

def test():
    from src.MosaicAI.Agents.Agent.Agent import Agent
    from src.MosaicAI.Agents.IMDBot.IMDBot import IMDBot
    from src.MosaicAI.Agents.RQE import RouterQueryEngine
    Agent()
    IMDBot()
    RouterQueryEngine()
    return True

__name__ == "__main__" and launch()
