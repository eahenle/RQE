from FrontEnd import FrontEnd

def launch():
    FrontEnd().run()

def test():
    from Agent import Agent
    from IMDBot import IMDBot
    from RQE import RouterQueryEngine
    Agent()
    IMDBot()
    RouterQueryEngine()
    return True

__name__ == "__main__" and launch()
