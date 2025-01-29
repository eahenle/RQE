def test():
    """
    Test the MosaicAI system.
    """

    # test instantiation of the Agent class
    from src.MosaicAI.Agent.Agent import Agent
    Agent()

    # test instantiation of the IMDBot class
    from src.MosaicAI.Agent.IMDBot.IMDBot import IMDBot
    IMDBot()

    # test instantiation of the RouterQueryEngine class
    from src.MosaicAI.Agent.RouterQueryEngine.RouterQueryEngine import RouterQueryEngine
    RouterQueryEngine()

if __name__ == "__main__":
    test()
    print("All tests passed!")
