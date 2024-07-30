import flowController
import numpy as np

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


def board_solver_simulated_annealing(controller):
    board = gameBoard.board_obj

    temperature = 100

    cooling_rate = .999

    current_score = evaluateBoard()

    roots = board.rootMap

    while temperature > 1:

        moves = {
            0: (-1, 0),  # up
            1: (1, 0),  # down
            2: (0, -1),  # left
            3: (0, 1)  # right
        }

        # 0 will be up, 1 down, 2 left, 3 right
        next_move = np.random.choice(0, 1, 2, 3)

        new_i, new_j = moves[next_move]

        selected_color = np.random.choice(list(roots.keys()))

        selected_root = roots[selected_color][-2]

        new_node_i = selected_root.x + new_i
        new_node_j = selected_root.x + new_j

        try:
            board.extendPath(selected_root.x, selected_root.y, new_node_i, new_node_j)
            updated_score = evaluateBoard()

            if updated_score < current_score or np.random.uniform(0, 1) <= np.exp(
                    (current_score - updated_score) / temperature):
                current_score = updated_score
                roots[selected_color].insert(len(roots[selected_color]) - 1, (new_node_i, new_node_j))
            else:
                board.removeNode(new_i, new_j)
            temperature *= cooling_rate
        except:
            continue
