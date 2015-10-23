from message import Message

class Classifier:
    def __init__(self):
        self.rule = []
        self.output = []

    def check_activate( self, messages ):
    """Return true if the message activates the rule."""
        for m in messages:
            if ( m.rule_matches(self) ):
                return True
        return False
                
