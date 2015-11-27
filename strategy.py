##
## Different strategies to be used by the bot. The strategies
## are mutually exclusive i.e. only one of them can be active
## at a time
##

from collections import deque

from game import Game

## used by 'classifier' based strategy
from message import Message
from classifier import Classifier
from classifier_system import ClassifierSystem

class Strategy:
    """Base class for different strategies that can
    be tried out by the bot
    """
    def init(self, game):
        """Intitialize the strategy object
        """
        self.game = game

        # game state
        self.expected_pos = self.game.hero.pos
        self.prev_mines = 0
        self.prev_gold = 0
        self.prev_life = 100
        self.action = 'Wait'

    def cleanup(self):
        """Do the cleanup actions specific to the
        'strategy' here.
        """
        pass

    def next(self):
        """Use the game state to decide the next move.

        Moves can be one of-
         'Stay', 'North', 'South', 'East', 'West'
        """

        self.action = self.compute_action()
        move = self._next_move(self.action)
        self._post_action(move)
        return move

    def _next_move(self, action):
        """ Pick a move based on the given 'action'

        Supported actions are :-
         'Stay', 'Heal', 'Attack', 'Wait', 'Mine'

        Moves can be one of
         'Stay', 'North', 'South', 'East', 'West'
        """
        next_move = 'Stay' #default

        if action == 'Heal':
            if self.game.board.taverns_list[0].path:
                next_move = self.game.board.taverns_list[0].path[0]
        elif action == 'Mine':
            if self.game.board.mines_list[0].path:
                next_move = self.game.board.mines_list[0].path[0]
        elif action == 'Attack':
            if self.game.enemies_list[0].path:
                next_move = self.game.enemies_list[0].path[0]
        elif action == 'Wait':
                next_move = 'Stay'

        return next_move

    def _compute_action(self):
        """Decide the action to take based on the
        current game state.

        Supported actions are :-
         'Stay', 'Heal', 'Attack', 'Wait', 'Mine'

        Subclasses should override this method to
        implement specific logic.
        """
        # stand frozen with fear!
        return 'Stay'

    def _post_action(self, next_move):
        """Subclasses can override this method to
        implement class specific behavior.
        """

        # update game state kept locally in the bot
        self.expected_pos = self.game.board.to(self.game.hero.pos, next_move)
        self.prev_mines = self.game.hero.mines
        self.prev_gold = self.game.hero.gold
        self.prev_life = self.game.hero.life

class RandomStrategy(Strategy):
    """Naive strategy which chooses an action at
    random.
    """

class ClassifierStrategy(Strategy, ClassifierSystem):
    """Uses a system of message based classififiers to
    decide the optimum move. In each iteration, a
    genetic algorithm is used to evolve the classifiers.
    """
    def __init__(self, key):
        self.key = key

    def init(self, game):
        """Intitialize the strategy object
        """

        Strategy.init(self, game)

        self.input_interface = []
        ClassifierSystem.__init__(self)


        self.new_game()

    def cleanup(self):
        """Method called when a game ends. Do the
        class specific cleanups here
        """

        self.finish_game()

    def compute_action(self):
        """Returns the direction in which the bot is to move.
        """

        message = Message()
        message.game_message(self.game, self.action)

        self.input_interface.append(message)

        return self.decide()
