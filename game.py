import re

from collections import deque
import heapq

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
        self.threat_map = [ [0 for i in range(self.board.size)] for j in range(self.board.size)]
        self.enemies = {}
        for i in range(len(state['game']['heroes'])):
            if ( state['game']['heroes'][i]['id'] != state['hero']['id'] ):
                new_enemy = Hero( state['game']['heroes'][i] )
                print "enemy position %d %d" % (new_enemy.pos[0],new_enemy.pos[1])
                self.enemies[new_enemy.pos] = new_enemy

        self.hero = Hero(state['hero'])
        self.dijkstra ()

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
        self.dijkstra()

    def get_path( self, node ):
        path = []
        distance, loc, this_node = node
        while ( this_node ):
            to_row, to_col = loc
            distance, loc, this_node = this_node
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
        frontier_queue.append( (0, self.hero.pos, None) )
        frontier_dict[self.hero.pos] = (0, self.hero.pos, None)

        while ( frontier_queue ):
            node = frontier_queue.popleft()
            distance, loc, parent = node
            
            del frontier_dict[loc]
            explored[loc] = node

            for direction,coords in enumerate(AIM):
                next_loc = self.board.to(loc, coords)
                if next_loc:
                    next_node = ( distance + 1, next_loc, node )
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

    def threat_update(self):
        self.threat_map = [ [0 for i in range(self.board.size)] for j in range(self.board.size)]
        enemy_num = 0;
        for pos,enemy in self.enemies.iteritems():
            enemy_num+=1
            threat = 5
            frontier_queue = deque([])
            frontier_dict = {}
            frontier_dict[enemy.pos] = (threat, enemy.pos)
            explored = {}
            frontier_queue.append( (threat, enemy.pos ) )
            self.threat_map[enemy.pos[0]][enemy.pos[1]] = threat
            while threat > 1 and frontier_queue:
                node = frontier_queue.popleft()
                threat, loc = node
                threat -= 1
                del frontier_dict[loc]
                explored[loc] = node
                for direction,coords in enumerate(AIM):
                    next_loc = self.board.to(loc, coords)
                    if next_loc:
                        next_node = ( threat, next_loc )
                        if (next_loc not in explored
                                and next_loc not in frontier_dict
                                and self.board.passable(next_loc)):
                            self.threat_map[next_loc[0]][next_loc[1]] += threat
                            frontier_queue.append( next_node )
                            frontier_dict[next_loc] = next_node
        #for m in self.threat_map:
            #for token in m:
                #print token,
            #print "\""
    def dijkstra(self):
        "Claculate paths taking tile threat values into account"
        self.threat_update()
        frontier_queue = []
        frontier_dict = {}
        explored = {}
        heapq.heappush(frontier_queue, (0, self.hero.pos, None) )
        frontier_dict[self.hero.pos] = (0, self.hero.pos, None)

        while ( frontier_queue ):
            node = heapq.heappop(frontier_queue)
            distance, loc, parent = node
            
            del frontier_dict[loc]
            explored[loc] = node

            for direction,coords in enumerate(AIM):
                next_loc = self.board.to(loc, coords)
                if next_loc:
                    next_node = ( distance + 1 + self.threat_map[next_loc[0]][next_loc[1]], next_loc, node )
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
                        heapq.heappush(frontier_queue, next_node )
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

