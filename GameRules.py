from ParseBoard import read_boards
import numpy as np

boards = read_boards("Puzzles/8by8Puzzles.txt")
board = boards[0]


class Node:
    #initializes a node with x,y coordinates, a value, a color based on value, a boolean root based on value,
    # and the previous and next nodes for its path
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.color = self.determine_color()
        #boolean True if it is a root
        self.root = self.value != "."
        self.previous = None
        self.next = None

    def determine_color(self):
        color_mapping = {
            '.': (0, 0, 0),
            'A': (255, 0, 0),  # Red
            'B': (0, 0, 255),  # Blue
            'C': (0, 255, 0),  # Green
            'D': (255, 255, 0),  # Yellow
            'E': (128, 0, 128),  # Purple
            'F': (255, 165, 0),  # Orange
            'G': (255, 192, 203),  # Pink
            'H': (0, 255, 255),  # Cyan
            'I': (255, 0, 255),  # Magenta
            'J': (139, 69, 19),  # Brown
            'K': (128, 128, 128),  # Gray
            'L': (255, 255, 255),  # White
            # add colors as needed
        }
        return color_mapping.get(self.value, (169, 169, 169))



class Board:
    def __init__(self, board):
        self.board = [
            [Node(board[x][y], x, y) for y in range(len(board[0]))]
            for x in range(len(board))
        ]

    def validPos(self, x, y):
        if 0 < y < self.board.size and 0 < x < self.board[0].size:
            return True
        else:
            return False

    def boardFilled(self):
        flag = True
        for x in self.board[0].size:
            for y in self.board.size:
                if self.board[y][x].color == "Black":
                    flag = False
        return flag

    #Changes the color, previous, and next of node in position I,J
    #The original node is X,Y and the path we are extending to is I,J
    #Checks to see if I,J is in a valid position
    #Checks the X,Y and I,J are adjacent
    #
    def extendPath(self, x, y, i, j):
        if not self.validPos(i, j):
            raise Exception("Not a valid position")
        original = board[x][y]
        new = board[i][j]
        #Makes sure that the nodes are adjacent
        if np.absolute(x - i) != 1 or np.absolute(y - j) != 1:
            raise Exception("Not a continous path")
        #Checks for mulitdirectional pathing from a root
        if original.root and original.path.size > 1:
            raise Exception("Root path is not empty")
        #Checks for new square being another color's root
        if new.root and original.color != new.color:
            raise Exception("Cannot overide a root")
        if original.next.color != "Black":
            raise Exception("Paths cannot diverge")

        original.next = new
        new.color = original.color
        new.previous = original


test_board = Board(board=board)

# board = np.array([1,2,3,4])
# board.size
