class WanderState(object):

    def __init__(self, avatar):
        self.avatar = avatar
        pass

    def enter(self):
        print "Entered Wander State."
        pass

    # We'll stay in the wander state until we can "see" the other player
    # via some radial distance metric.
    def execute(self):
        pass

    def exit(self):
        print "Exited Wander State."
        pass