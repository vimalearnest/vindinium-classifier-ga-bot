#
# The bot playing the game
#
from game import Game

class TesterBot3000:
    def __init__(self, key, strategy):
        """Initialize the bot with the given strategy
        """

        self.key = key
        self.strategy = strategy

    def new_game(self, state):
        """Initialize the bot with a new game."""

        self.game = Game(state)

        print "I am player %s" % self.game.hero.ident
        print "My position is at (%s, %s)" % self.game.hero.pos


        self.strategy.init(self.game)

    def finish_game(self):
        """Cleanup game state, book keeping stuff etc.
        """

        self.strategy.cleanup()


    def move(self, state):
        """Use the game state to decide the next move.

        Moves can be one of-
         'Stay', 'North', 'South', 'East', 'West'
        """

        self.game.update(state)

        next_move = self.strategy.next()

        return next_move
