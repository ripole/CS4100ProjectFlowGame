import flowController

gameBoard = flowController.Controller('8by8Puzzles.txt')


def evaluateBoard():
    completedColors = []
    for roots in gameBoard.board_obj.rootMap.values():
        current = roots[0]
        if gameBoard.board_obj.connectedPath(gameBoard, current.x, current.y):
            completedColors.append(current.color)
        else:
            pointA = current
            if current.next:
                pointA = current.next
                while pointA.next:
                    pointA = pointA.next
            elif current.prev
