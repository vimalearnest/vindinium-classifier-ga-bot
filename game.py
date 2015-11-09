class Game:

    def __init__(self, state):
        """Initialize the game

        state - state of the game as returned by the API
        """

        self.update(state)

        
    def update(self, state):

        tiles = state['game']['board']['tiles']
        size = state['game']['board']['size']
        
        self.board = Board(tiles, size)
    

    def pr(self):
        """Print information about the game
        """

        self.board.pr()
            

class Board:
    """Representation of the game 'board' an 'n'x'n' tile
    """

    def __init__(self, tiles, size):
        """Initialize the game board

        tile - string representation of the tiles 
        size - no of tiles
        """

        self.size = size
        self.tiles = self.parse_tiles(tiles)

        # main pieces in the game
        self.taverns = []
        self.mines = []
        self.enemies = []

    def parse_tiles(self, tiles):
        """Splits the strng representation of tiles
        into rows and columns accessible by [row][col]
        """

        # split the string into rows 
        chars_in_row = self.size * 2
        rows = [tiles[i:i+chars_in_row] for i in range(0, len(tiles), chars_in_row)]
 
        # split each of the rows into columns
        return [[row[i:i+2] for i in range(0, len(row), 2)] for row in rows]

    def pr(self):
        """Print the pieces on the board
        """        
        
        print '-' * (self.size+1) * 2
        for row in range(self.size):
            print '|' + ''.join(self.tiles[row]) + '|'
        print '-' * (self.size+1) * 2   

