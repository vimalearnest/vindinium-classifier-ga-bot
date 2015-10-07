import re

from collections import deque

TAVERN = 0
AIR = -1
WALL = -2
MINE = -3

PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

AIM = {'North': (-1, 0),
       'East':  ( 0, 1),
       'South': ( 1, 0),
       'West':  ( 0,-1)}
REVERSE_AIM = {(-1,0): 'South',
               (0, 1): 'West',
               (1, 0): 'North',
               (0,-1): 'East',
               (0, 0): 'Stay'}

class Game:
    def __init__(self, state):
        self.state = state
        self.board = Board(state['game']['board'])
        self.enemies = {}
        for i in range(len(state['game']['heroes'])):
            if ( state['game']['heroes'][i]['id'] != state['hero']['id'] ):
                new_enemy = Hero( state['game']['heroes'][i] )
                self.enemies[new_enemy.pos] = new_enemy

        self.hero = Hero(state['hero'])
        self.bfs()

    def update(self, state):
        """Update paths, enemy positions, and mine ownership"""
        self.clear_paths()
        self.state = state
        self.enemies = {}
        for i in range(len(state['game']['heroes'])):
            if ( state['game']['heroes'][i]['id'] != state['hero']['id'] ):
                new_enemy = Hero( state['game']['heroes'][i] )
                self.enemies[new_enemy.pos] = new_enemy
        self.hero = Hero(state['hero'])
        for k,v in self.board.mines.iteritems():
            v.update_owner(state['game']['board']['tiles'])
        self.bfs()

    def get_path( self, node ):
        path = []
        loc, distance, this_node = node
        while ( this_node ):
            to_row, to_col = loc
            loc, distance, this_node = this_node
            from_row, from_col = loc
            path.append( REVERSE_AIM[(from_row-to_row,from_col-to_col)] )
        path.reverse()
        return path

    def clear_paths(self):
        for k,v in self.enemies.iteritems():
            v.path = None
        for k,v in self.board.taverns.iteritems():
            v.path = None
        for k,v in self.board.mines.iteritems():
            v.path = None


    def bfs(self):
        frontier_queue = deque([])
        frontier_dict = {}
        explored = {}
        frontier_queue.append( (self.hero.pos, 0, None) )
        frontier_dict[self.hero.pos] = (self.hero.pos, 0, None)

        while ( frontier_queue ):
            node = frontier_queue.popleft()
            loc, distance, parent = node
            
            del frontier_dict[loc]
            explored[loc] = node

            for direction,coords in enumerate(AIM):
                next_loc = self.board.to(loc, coords)
                if next_loc:
                    next_node = ( next_loc, distance + 1, node )
                    if next_loc in self.board.mines:
                        if not self.board.mines[next_loc].path:
                            self.board.mines[next_loc].path = self.get_path(next_node)
                            #print "Path to Mine = ",
                            #print self.board.mines[next_loc].path,
                            #print "  ",
                            #print next_loc
                    elif next_loc in self.enemies:
                        if not self.enemies[next_loc].path:
                            self.enemies[next_loc].path = self.get_path(next_node)
                            #print "Path to enemy = ",
                            #print self.enemies[next_loc].path,
                            #print "  ",
                    elif next_loc in self.board.taverns:
                        if not self.board.taverns[next_loc].path:
                            self.board.taverns[next_loc].path = self.get_path(next_node)
                            #print "Path to Tavern = ",
                            #print self.board.taverns[next_loc].path,
                            #print "  ",
                    elif (next_loc not in explored
                            and next_loc not in frontier_dict
                            and self.board.passable(next_loc)):
                        frontier_queue.append( next_node )
                        frontier_dict[next_loc] = next_node


        


class Tavern:
    def __init__(self):
        self.path = None

class Mine:
    def __init__(self, owner_char_index):
        self.path = None
        self.owner = None
        self._owner_char_index = owner_char_index

    def update_owner(self, tiles):
        if '-' == tiles[self._owner_char_index]:
            self.owner = None
        else:
            self.owner = int(tiles[self._owner_char_index])

class Board:
    def _parseTile(self, row, col, token):
        if (token == '  ' or token[0] == '@'):
            return AIR
        if (token == '##'):
            return WALL
        if (token == '[]'):
            self.taverns[(row,col)] = Tavern()
            return TAVERN
        if (token[0] == '$'):
            self.mines[(row,col)] = Mine( row*self.size*2 + col*2 + 1 )
            return MINE

    def _parseTiles(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]
        self.print_board(tiles)

        return [[self._parseTile(row, col, x) for col, x in enumerate(xs)] for row, xs in enumerate(matrix)]

    def __init__(self, board):
        self.size = board['size']
        self.taverns = {}
        self.mines = {}
        self.tiles = self._parseTiles(board['tiles'])

    def passable(self, loc):
        'true if can not walk through'
        x, y = loc
        pos = self.tiles[x][y]
        return pos == AIR

    def to(self, loc, direction):
        'calculate a new location given the direction'
        row, col = loc
        d_row, d_col = AIM[direction]
        n_row = row + d_row
        if (n_row < 0): return None
        if (n_row >= self.size): return None
        n_col = col + d_col
        if (n_col < 0): return None
        if (n_col >= self.size): return None

        return (n_row, n_col)
    def print_board(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]
        for m in matrix:
            for token in m:
                print token,
            print "\""

class Hero:
    def __init__(self, hero):
        self.ident = hero['id']
        self.name = hero['name']
        self.pos = (hero['pos']['x'],hero['pos']['y'])
        self.spawn = (hero['spawnPos']['x'],hero['spawnPos']['y'])
        self.life = hero['life']
        self.gold = hero['gold']
        self.path = None

