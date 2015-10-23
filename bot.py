from game import Game
from message import Message
from classifier import Classifier

class Bot:
    pass

class TesterBot3000(Bot):
    def __init__(self):
        """Initialize the classifiers."""
        self.classifiers = []
        self.classifiers.append( Classifier() )
        self.classifiers.append( Classifier() )
        self.classifiers.append( Classifier() )
        self.classifiers[0].rule = [ [0, 1, 2] ]
        self.classifiers[0].output = 'Heal'
        self.classifiers[1].rule = [ None, None, [0,1], [0,1], [1,2,3,4,5] ]
        self.classifiers[1].output = 'Attack'
        self.classifiers[2].rule = [ ]
        self.classifiers[2].output = 'Mine'
    def new_game(self, state):
        """Initialize the bot with a new game."""
        self.game = Game(state)
        print "I am player",
        print self.game.hero.ident
        print "My position",
        print self.game.hero.pos

    def move(self, state):
        """Use the game state to decide what action to take, and then output the direction to move."""
        self.game.update(state)
        print "Score :",
        print self.game.hero.gold,
        for pos,b in self.game.enemies.iteritems():
            print b.gold,
        print ""

        self.game.board.print_board(state['game']['board']['tiles'])

        messages = [ Message(self.game) ]
        action = 'Stay'
        retval = 'Stay'
        for c in self.classifiers:
            if ( c.check_activate(messages) ):
                action = c.output
                break
        print "Action: ",
        print action
        if ( action == 'Heal' ):
            if ( None != self.game.board.taverns_list[0].path ):
                retval = self.game.board.taverns_list[0].path[0]
            else:
                action = 'Mine'
        if ( action == 'Mine' ):
            if ( None != self.game.board.mines_list[0].path ):
                retval = self.game.board.mines_list[0].path[0]
                print "Mine's value : ",
                print self.game.board.mines_list[0].value
            else:
                action = 'Attack'
        if ( action == 'Attack' ):
            if ( None != self.game.enemies_list[0].path ):
                retval = self.game.enemies_list[0].path[0]
        print "post Action: ",
        print action
        print "output: ",
        print retval



        return retval



