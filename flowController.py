import GameRules as modelClass
from ParseBoard import read_boards
import View as viewClass


class Player:
    def __init__(self, filename):
        self.board = modelClass.Board(read_boards(filename))
        self.view = viewClass.View(self.board)

    def isGameOver(self):
        return self.board.gameOver()

    def makeMove(self, x, y, i, j):
        self.board.extendPath(x, y, i, j)
        self.view.draw_board(self.board)



