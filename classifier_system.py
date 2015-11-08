from game import Game
from message import Message
from classifier import Classifier
from collections import deque

import random

class ClassifierSystem:
    def __init__(self):
        self.classifiers = self._get_test_classifiers()
        self.active = deque([])

    def _get_test_classifiers(self):
        c = [ Classifier() for x in range(7) ]

        # If you are less than 1/2 life, go heal
        c[0].identifier = 'heal 1/2 life'
        c[0].conditions.append( [ None ] * len( Message.game_msg_index) )
        c[0].conditions[0][Message.game_msg_index['source']] = [0]
        c[0].conditions[0][Message.game_msg_index['life']] = [0, 1, 2]
        c[0].specifity = 8
        c[0].output = None, 'Heal'

        # If enemy has atleast 1 mine, has less health than you, and is within 2 steps
        # attack him
        c[1].identifier = 'Attack close1'
        c[1].conditions.append( [ None ] * len( Message.game_msg_index) )
        c[1].conditions[0][Message.game_msg_index['source']] = [0]
        c[1].conditions[0][Message.game_msg_index['near_dist']] = [0, 1]
        c[1].conditions[0][Message.game_msg_index['near_life']] = [0, 1, 2]
        c[1].conditions[0][Message.game_msg_index['near_mine']] = [1, 2, 3, 4, 5]
        c[1].specifity = 13
        c[1].output = None, 'Attack'

        # If you have more than 1/2 life, mine
        c[2].identifier = 'Mine Standard'
        c[2].conditions.append( [ None ] * len( Message.game_msg_index) )
        c[2].conditions[0][Message.game_msg_index['source']] = [0]
        c[2].conditions[0][Message.game_msg_index['life']] = [3, 4, 5]
        c[2].specifity = 8
        c[2].output = None, 'Mine'

        # If you are next to a mine, and don't have max life, heal
        c[3].identifier = 'Heal at taver'
        c[3].conditions.append( [ None ] * len( Message.game_msg_index) )
        c[3].conditions[0][Message.game_msg_index['source']] = [0]
        c[3].conditions[0][Message.game_msg_index['life']] = [0, 1, 2, 3, 4]
        c[3].conditions[0][Message.game_msg_index['tavern_dist']] = [0]
        c[3].specifity = 11
        c[3].output = None, 'Heal'

        # If you have more mines than anyone else, and there is an enemy
        # approaching, go to the nearest tavern
        c[4].identifier = 'enemy coming '
        c[4].conditions.append( [ None ] * len( Message.game_msg_index) )
        c[4].conditions[0][Message.game_msg_index['source']] = [0]
        c[4].conditions[0][Message.game_msg_index['rel_mines']] = [3, 4, 5]
        c[4].conditions[0][Message.game_msg_index['tavern_enemy_relative_distance']] = [0, 1, 2, 3]
        c[4].specifity = 10
        c[4].output = None, 'Heal'

        # Idling rule
        c[5].identifier = 'Idle         '
        c[5].conditions.append( [ None ] * len( Message.game_msg_index) )
        c[5].conditions[0][Message.game_msg_index['source']] = [0]
        c[5].specifity = 5
        c[5].output = None, 'RandomWalk'

        # A bad rule, should lose strength
        c[6].identifier = 'Bad attack   '
        c[6].conditions.append( [ None ] * len( Message.game_msg_index) )
        c[6].conditions[0][Message.game_msg_index['source']] = [0]
        c[6].conditions[0][Message.game_msg_index['life']] = [0,1,2]
        c[6].conditions[0][Message.game_msg_index['near_dist']] = [0,1,2]
        c[6].conditions[0][Message.game_msg_index['near_life']] = [3,4,5]
        c[6].specifity = 15
        c[6].output = None, 'Attack'
        return c

    def _weighted_choice( self, choices ):
        """Choose one of choices proportional to the strength values"""
        total = sum( strength for strength, out, sources in choices )
        r = random.uniform(0,total)
        upto = 0
        for strength , c, sources in choices:
            if upto + strength > r:
                return strength, c.output[1]
            upto += strength
        return None

    def _disburse( self, amount ):
        """Disburse the credit to the active classifiers"""
        for x in self.active:
            for y in x:
                c, source_classifiers = y
                c.pay( amount / float(len(self.active)) )
                for z in source_classifiers:
                    z.pay( amount / float(len(source_classifiers)) )


    def _credit_allocation( self ):
        """Give credit to the current situation to the active classifiers"""
        # Payoff results from previous turn
        # Detect Death
        # TODO this does not work if you die on your spawn point
        if ( self.game.hero.pos != self.expected_pos
             and self.game.hero.pos == self.game.hero.spawn ):
             self._disburse(-100 * self.prev_mines / float(len(self.game.board.mines_list)))
             self.active = deque([])
        # If you didn't die, pay active classifers by the amount of gold gained
        else:
            # If you captured a mine, reward
            if ( self.game.hero.mines > self.prev_mines ):
                self._disburse(10 * (self.game.hero.mines - self.prev_mines) )

            # For each currently owned mine
            self._disburse( self.game.hero.mines )

        if ( len(self.active) > 19 ):
            self.active.popleft()

    def _print_classifier_status( self ):
        """Output for debugging"""
        print "Classifier info"
        for c in self.classifiers:
            count = 0
            for b in self.active:
                for a in b:
                    if a[0] == c:
                        count += 1
            print c.identifier,
            print count,
            print c.strength
        print ""

    def decide( self ):
        """Decide what action to take this turn"""
        self._credit_allocation();
        
        # Process the input_interface Messages
        matches = []
        messages = self.input_interface[:]
        self.input_interface = []

        # Find all classifiers that match the input messages
        print "match",
        for c in self.classifiers:
            if ( c.check_activate(messages) ):
                print c.identifier,
                print ",",
                message, action = c.output
                if ( None == action ):
                    c.pay(c.bid())
                    if ( None != message ):
                        self.input_interface.append( message )
                else:
                    matches.append( ( c.bid(), c, c.source_classifiers ) )
        print ""

        # TODO if not enough matches, create more classifiers

        # Choose an action from the matches to output
        choice = self._weighted_choice(matches)
        print "choice",
        print choice

        # activate all of the classifiers that specified the chosen action
        # and send any output messages to the input interface
        if ( None != choice ):
            paid, winner = choice
            activated = []
            for m in matches:
                bid, c, source_classifiers = m
                if c.output[1] == winner:
                    activated.append( (c, source_classifiers ) )
                    c.pay(-paid)
                    message, action = c.output
                    if ( None != message ):
                        self.input_interface.append( message )
            self.active.append(activated)
            return action
        else:
            return 'None'


