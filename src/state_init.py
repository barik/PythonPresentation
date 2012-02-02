from src.state_wander import WanderState

class InitState(object):

    def __init__(self, avatar):
        self.avatar = avatar

    def enter(self):
        print "Entered Initial State."
        pass

    def execute(self):
        self.avatar.changeState(WanderState(self.avatar))
        pass

    def exit(self):
        print "Exited Initial State."
        pass
