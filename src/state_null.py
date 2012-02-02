# The Null State is only used for player-controlled characters.
# Since the player is in complete control, it really doesn't do anything
# at all.

# See Programming Game AI by Example for this model of FSM.

class NullState(object):

    def __init__(self, avatar):

        self.avatar = avatar
        pass

    # Name of the state to avoid checking object types.
    def name(self):
        return "Null State"

    def enter(self):
        print "Entered Null State, and will stay here."
        pass

    def execute(self):
        pass

    def exit(self):
        print "Shouldn't ever exit Null State."
        pass

    pass