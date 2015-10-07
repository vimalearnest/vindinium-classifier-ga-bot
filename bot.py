from game import Game

class Bot:
    pass

class TesterBot3000(Bot):
    def new_game(self, state):
        self.game = Game(state)
        print "I am player",
        print self.game.hero.ident
        print "My position",
        print self.game.hero.pos

    def move(self, state):
        self.game.update(state)
        print "Score :",
        print self.game.hero.gold,
        for pos,b in self.game.enemies.iteritems():
            print b.gold,
        print ""

        self.game.board.print_board(state['game']['board']['tiles'])


        retval = 'Stay'
        chosen_path_length = 999
        if self.game.hero.life > 50:
            print "mining"
            for pos,mine in self.game.board.mines.iteritems():
                if (mine.owner != self.game.hero.ident
                    and mine.path
                    and len(mine.path) < chosen_path_length):
                    tmppos = pos
                    tmppath = mine.path
                    chosen_path_length = len(mine.path)
                    retval = mine.path[0]
            if retval != 'Stay':
                print "moving to mine at",
                print tmppos
                print "path =",
                print tmppath
        else:
            print "healing"
            for pos,tavern in self.game.board.taverns.iteritems():
                if (tavern.path
                    and len(tavern.path) < chosen_path_length):
                    tmppos = pos
                    tmppath = tavern.path
                    chosen_path_length = len(tavern.path)
                    retval = tavern.path[0]
            if retval != 'Stay':
                print "moving to tavern at",
                print tmppos
                print "path =",
                print tmppath

        return retval



