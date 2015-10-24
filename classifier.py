from message import Message

class Classifier:
"""A classifier consists of two parts.
  1. The rule is used to match against messages for when the classifier activates.
  2. The output consists of a list of messages to be added to the message queue"""
# TODO add classifier strength as described in the paper.

# NOTE Rules are created using the following alphabet
# {None(Matches any value), [0], [1], [2], [3], [4], [5],
#   [0,1], [0,2], [0,3], [0,4], [0,5],
#   [1,2], [1,3], [1,4], [1,5],
#   [2,3], [2,4], [2,5],
#   [3,4], [3,5],
#   [4,5],
#   [0,1,2], [0,1,3] [0,1,4], [0,1,5], [0,2,3], [0,2,4], [0,2,5], [0,3,4], [0,3,5], [0,4,5],
#   [1,2,3], [1,2,4], [1,2,5], [1,3,4], [1,3,5], [1,4,5],
#   [2,3,4], [2,3,5], [2,4,5],
#   [3,4,5],
#   [0,1,2,3], [0,1,2,4], [0,1,2,5], [0,1,3,4], [0,1,3,5], [0,1,4,5], [0,2,3,4], [0,2,3,5], [0,2,4,5], [0,3,4,5],
#   [1,2,3,4], [1,2,3,5], [1,2,4,5], [1,3,4,5],
#   [2,3,4,5],
#   [0,1,2,3,4], [0,1,2,3,5], [0,1,2,4,5], [0,1,3,4,5], [0,2,3,4,5],
#   [1,2,3,4,5] }

    def __init__(self):
        self.rule = []
        self.output = []

    def check_activate( self, messages ):
    """Return true if the message activates the rule."""
        for m in messages:
            if ( m.rule_matches(self) ):
                return True
        return False
                
