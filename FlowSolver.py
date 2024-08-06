import numpy as np
import random
import copy

moves = {
    0: (-1, 0),  # up
    1: (1, 0),  # down
    2: (0, -1),  # left
    3: (0, 1),  # right
}

def evaluateBoard(controller):
    board = controller.board_obj
    cornerList = [
        [0, 0],
        [0, len(board.board) - 1],
        [len(board.board[0]) - 1, 0],
        [len(board.board[0]) - 1, len(board.board) - 1],
    ]
    corners = 0
    completedColors = []
    distance = 0
    blocked = 0
    for roots in board.paths.values():
        pointA = roots[0][-1]
        pointB = roots[1][-1]
        if board.connectedPath(roots[0][0].value):
            completedColors.append(roots[0][0].value)
        else:
            Ax, Ay = pointA.pos
            Bx, By = pointB.pos
            distance += abs(Ax - Bx) + abs(Ay - By)
            if (
                len(get_available_moves(board, pointA.pos)) == 0
                or len(get_available_moves(board, pointB.pos)) == 0
            ):
                blocked = 1000
        for coords in cornerList:
            if get_available_moves(board, coords) is None:
                corners = corners + 10
    empty_cell_score = 0
    for row in board.board:
        for cell in row:
            if cell.color == (0, 0, 0):
                empty_cell_score += 5
    return (
        distance - len(completedColors) + blocked + corners + empty_cell_score,
        completedColors,
    )


def select_incomplete_color(controller, completedColors):
    all_colors = list(controller.board_obj.paths.keys())
    incomplete_colors = [color for color in all_colors if color not in completedColors]
    if incomplete_colors:
        return (np.random.choice(incomplete_colors),np.random.choice([0,1]))
    else:
        return None  # All colors are complete


# finding the most constrained path. Returns the color value and then which path it is in
def mostConstrainedPath(controller):
    board = controller.board_obj
    minMoves = 5
    minValue = []
    for roots in board.paths.values():
        if not board.connectedPath(roots[0][0].value):
            pointA = roots[0][-1]
            pointB = roots[1][-1]
            Avalue = len(get_available_moves(board, pointA.pos))
            Bvalue = len(get_available_moves(board, pointB.pos))
            if Avalue < minMoves:
                minMoves = Avalue
                minValue = [pointA.value, 0]
            if Bvalue < minMoves:
                minMoves = Bvalue
                minValue = [pointB.value, 1]
    return minValue


# Returns the path list of the closest paths
def findClosestPath(controller):
    board = controller.board_obj
    minDist = 9999999999
    minValue = None
    for roots in board.paths.values():
        if not board.connectedPath(roots[0][0].value):
            pointA = roots[0][-1]
            pointB = roots[1][-1]
            Ax, Ay = pointA.pos
            Bx, By = pointB.pos
            distance = abs(Ax - Bx) + abs(Ay - By)
            if distance < minDist:
                minDist = distance
                minValue = roots[0][0].value
    return minValue


def get_available_moves(board, pos):


    available_moves = []
    x, y = pos
    for move in moves.values():
        new_x, new_y = x + move[0], y + move[1]
        if board.validPos(new_x, new_y):
            neighbor_color = board.board[new_x][new_y].color
            if neighbor_color == (0, 0, 0):
                available_moves.append((new_x, new_y))
    return available_moves


def get_best_available(controller, pos, moves):
    best_score = 10000000
    best_move = moves[np.random.choice(range(len(moves)))]
    for move in moves:
        controller.makeDummyMove(pos, move)
        updated_score, completed_colors = evaluateBoard(controller)
        if updated_score <= best_score:
            best_score = updated_score
            best_move = move
        controller.dummyRemove(move)
    return best_move


def delete_path(controller, delete_path, random):
    if random:
        length = np.random.choice(range(len(delete_path)))
    else:
        length = len(delete_path) - 1
    for i in range(length):
        controller.remove(delete_path[-1].pos)

def get_constraining_path(controller, path):
    node = path[-1]
    value = node.value
    x,y = node.pos
    constraining_colors = []
    for move in moves:
        i,j = moves[move]
        if controller.board_obj.validPos(x+i,y+j):
            neighbor = controller.board_obj.board[x+i][y+j]
            if neighbor.value != value:
                constraining_colors.append(neighbor)
    index = np.random.choice(range(len([constraining_colors])))
    if constraining_colors:
        constrained_path = controller.board_obj.find_node_path(constraining_colors[index])
        return constrained_path
    else:
        return constraining_colors



def board_solver_simulated_annealing(controller):
    board = controller.board_obj

    roots = board.paths

    temperature = 100

    cooling_rate = 0.9

    current_score, completed_colors = evaluateBoard(controller)

    counter = 0

    completed_colors_count = 0

    while temperature > 1:

        if counter >= 30 and completed_colors:
            index = np.random.choice(range(len(completed_colors)))
            value = completed_colors[index]
            delete = roots[value][np.random.choice([0,1])]
            delete_path(controller, delete, False)
            completed_colors_count -= 1
            counter = 0

        if np.random.rand() >= .3:
            selected_color = mostConstrainedPath(controller)
        else:
            selected_color = select_incomplete_color(controller, completed_colors)

        if selected_color:
            selected_path = roots[selected_color[0]][selected_color[1]]

            available_moves = get_available_moves(
                controller.board_obj, selected_path[-1].pos
            )

            # This writes a check to see if
            while not available_moves:
                path = get_constraining_path(controller,selected_path)
                delete_path(controller,path,False)
                delete_path(controller,selected_path,False)
                available_moves = get_available_moves(
                    controller.board_obj, selected_path[-1].pos
                )
                temperature = 100

            best_pos = get_best_available(
                controller, selected_path[-1].pos, available_moves
            )
            print(available_moves)
            rand_pos = random.choice(available_moves)

            try:
                controller.makeMove(selected_path[-1].pos, best_pos)
                best_score, completed_colors = evaluateBoard(controller)
                controller.remove(best_pos)

                controller.makeMove(selected_path[-1].pos, rand_pos)
                rand_score, completed_colors = evaluateBoard(controller)
                controller.remove(rand_pos)

                if completed_colors_count < len(completed_colors):
                    completed_colors_count += 1
                    counter = 0

                if np.random.uniform(0, 1) <= np.exp(
                    (best_score - rand_score) / temperature
                ):
                    best_pos = rand_pos

                controller.makeMove(selected_path[-1].pos, best_pos)
                temperature *= cooling_rate
            except:
                temperature *= cooling_rate
            counter += 1
        else:
            break
