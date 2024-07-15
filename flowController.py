from GameRules import model

def isGameOver():
     return gameOver()

def makeMove(x,y,i,j):
     extendPath(x,y,i,j)
     updateView(getBoard())


def updateView(board):
     draw_board(board)