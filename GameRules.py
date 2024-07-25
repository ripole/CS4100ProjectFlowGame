import numpy as np


def read_boards(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    boards = []
    i = 1
    while i < len(lines):
        # Read the size of the board
        size_line = lines[i].strip()
        if size_line:
            sizes = size_line.split()
            rows = int(sizes[1])
            board = []
            for j in range(i + 1, i + 1 + rows):
                board.append(list(lines[j].strip()))
            boards.append(board)
            i += rows + 1
        else:
            i += 1

    return boards



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
        self.path = []

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
        self.board_width = len(self.board[0])
        self.board_height = len(self.board)

    def validPos(self, x, y):
        return 0 <= x < self.board_width and 0 <= y < self.board_height

    def boardFilled(self):
        for row in self.board:
            for node in row:
                if node.color == "Black":
                    return False
        return True

    #Changes the color, previous, and next of node in position I,J
    #The original node is X,Y and the path we are extending to is I,J
    #Checks to see if I,J is in a valid position
    #Checks the X,Y and I,J are adjacent
    #
    def extendPath(self, x, y, i, j):
        if not self.validPos(i, j):
            raise Exception("Not a valid position")
        original = self.board[y][x]
        new = self.board[j][i]
        #Makes sure that the nodes are adjacent
        if  np.abs(x - i) + np.abs(y - j) != 1:
            raise Exception("Not a continous path")
        #Checks for mulitdirectional pathing from a root
        if original.root and len(original.path) >= 1:
            raise Exception("Root path is not empty")
        #Checks for new square being another color's root
        if new.root and original.color != new.color:
            raise Exception("Cannot overide a root")

        original.next = new
        original.path.append(new)
        new.color = original.color
        new.previous = original
        new.next = None

    #Checks to see if starting root is a connected to the ending node
    def connectedPath(self, x, y):
        node = self.board[x][y]
        flag = False
        if not node.root:
            raise Exception("connectedPath must start on root node")
        while node.next != None:
            if node.next.root:
                flag = True
            node = node.next
        return flag

    #Checks to see if the board is completed
    def gameOver(self):
        for x in self.board.size:
            for y in self.board[0].size:
                if self.board[x][y].root:
                    if not self.connectedPath(x, y):
                        return False
        return True

boards = read_boards("Puzzles/8by8Puzzles.txt")
test_board = boards[0]
test_Board = Board(board=test_board)

# board = np.array([1,2,3,4])
# board.size
