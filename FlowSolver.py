import flowController

gameBoard = flowController.Controller('8by8Puzzles.txt')

def findEndNode(root):
    current = root
    if current.next:
        while current.next:
            current = current.next
    elif current.prev:
        while current.prev:
            current = current.prev
    return current

def evaluateBoard():
    completedColors = []
    distance = 0
    for roots in gameBoard.board_obj.rootMap.values():
        if gameBoard.board_obj.connectedPath(gameBoard, roots[0].color):
            completedColors.append(roots[0].color)
        else:
            pointA = findEndNode(roots[0])
            pointB = findEndNode(roots[1])
            distance += abs(pointA.x - pointB.x) + abs(pointA.y - pointB.y)
    return distance + len(completedColors)
