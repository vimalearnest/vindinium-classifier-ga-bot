from game import Game
from message import Message
from classifier import Classifier

import random

class Bot:
    pass

def get_test_classifiers():
    c = [ Classifier() for x in range(5) ]

    # If you are less than 1/2 life, go heal
    c[0].conditions.append( [ None ] * len( Message.game_msg_index) )
    c[0].conditions[0][Message.game_msg_index['source']] = [0]
    c[0].conditions[0][Message.game_msg_index['life']] = [0, 1, 2]
    c[0].output = ['Heal']

    # If you are next to a mine, and don't have max life, heal
    c[3].conditions.append( [ None ] * len( Message.game_msg_index) )
    c[3].conditions[0][Message.game_msg_index['source']] = [0]
    c[3].conditions[0][Message.game_msg_index['life']] = [0, 1, 2, 3, 4]
    c[3].conditions[0][Message.game_msg_index['tavern_dist']] = [0]
    c[3].output = ['Heal']
    # If enemy has atleast 1 mine, has less health than you, and is within 2 steps
    # attack him
    c[1].conditions.append( [ None ] * len( Message.game_msg_index) )
    c[1].conditions[0][Message.game_msg_index['source']] = [0]
    c[1].conditions[0][Message.game_msg_index['near_dist']] = [0, 1]
    c[1].conditions[0][Message.game_msg_index['near_life']] = [0, 1, 2]
    c[1].conditions[0][Message.game_msg_index['near_mine']] = [1, 2, 3, 4, 5]
    c[1].output = ['Attack']

    # If you have more than 1/2 life, mine
    c[2].conditions.append( [ None ] * len( Message.game_msg_index) )
    c[2].conditions[0][Message.game_msg_index['source']] = [0]
    c[2].conditions[0][Message.game_msg_index['life']] = [3, 4, 5]
    c[2].output = ['Mine']
    # If you have more mines than anyone else, and there is an enemy
    # approaching, go to the nearest tavern
    c[4].conditions.append( [ None ] * len( Message.game_msg_index) )
    c[4].conditions[0][Message.game_msg_index['source']] = [0]
    c[4].conditions[0][Message.game_msg_index['rel_mines']] = [3, 4, 5]
    c[4].conditions[0][Message.game_msg_index['tavern_enemy_relative_distance']] = [0, 1, 2, 3]
    c[4].output = ['Heal']
    return c
class TesterBot3000(Bot):
    def __init__(self):
        """Initialize the bot's classifiers."""
        self.classifiers = get_test_classifiers()
        self.input_interface = []

    def new_game(self, state):
        """Initialize the bot with a new game."""
        self.game = Game(state)
        print "I am player",
        print self.game.hero.ident
        print "My position",
        print self.game.hero.pos

    def _weighted_choice( self, choices ):
        total = sum( strength for strength, out in choices )
        r = random.uniform(0,total)
        upto = 0
        for strength , out in choices:
            if upto + strength > r:
                return out
            upto += strength
        return None

    def move(self, state):
        """Use the game state to decide what action to take, and then output
           the direction to move."""
        self.game.update(state)
        print "Score :",
        print self.game.hero.gold,
        for pos,b in self.game.enemies.iteritems():
            print b.gold,
        print ""

        self.game.board.print_board(state['game']['board']['tiles'])

        message = Message()
        message.game_message(self.game)
        self.input_interface.append(message)
        outputs = []
        retval = 'Stay'

        # Process the input_interface Messages
        messages = self.input_interface[:]
        self.input_interface = []
        print "Classifiers matched",
        for c in self.classifiers:
            if ( c.check_activate(messages) ):
                for out in c.output:
                    print c.identifier,
                    if ( isinstance( out, basestring ) ):
                        outputs.append( ( c.strength, out ) )
                    else:
                        self.input_interface.append(out)
        print ""
        print "Classifier outputs",
        print outputs
        out = self._weighted_choice(outputs)
        print "Chosen output",
        print out
        if ( out == 'Heal' ):
            if ( None != self.game.board.taverns_list[0].path ):
                retval = self.game.board.taverns_list[0].path[0]
        elif ( out == 'Mine' ):
            if ( None != self.game.board.mines_list[0].path ):
                retval = self.game.board.mines_list[0].path[0]
        elif ( out == 'Attack' ):
            if ( None != self.game.enemies_list[0].path ):
                retval = self.game.enemies_list[0].path[0]
        print "output: ",
        print retval

        return retval



