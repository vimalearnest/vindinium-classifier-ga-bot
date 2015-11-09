from game import Game

import random

class Voltron2000:

    def new_game(self, state):
        """Initialize a new game
        """

        self.game = Game(state)
   
        hero = state['hero']

        self.ident = hero['id']
        self.name = hero['name']
        self.pos = hero['pos']['x'], hero['pos']['y']
        self.spawn_pos = hero['spawnPos']['x'], hero['spawnPos']['y']
        self.life = hero['life']
        self.gold = hero['gold']
        self.mines = hero['mineCount']

    def update(self, state):
        self.game.update(state)

    def move(self, state):
        """decide which move to take
        """
        
        options = ['Stay', 'North', 'South', 'East', 'West']
                 
        move = random.choice(options)
        return move

    def pr(self):
        """
        """
        self.game.pr()
        


