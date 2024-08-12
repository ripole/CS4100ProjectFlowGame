import numpy as np
import random
import copy
from scipy.ndimage import label


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
    adjacent = 0

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

        for paths in roots:
            if len(paths) != 1:
                adjacent = adjacent + adjacentCells(controller, paths)
    for coords in cornerList:
        if get_available_moves(board, coords) is None:
            corners = corners + 10
    empty_cell_score = 0
    for row in board.board:
        for cell in row:
            if cell.color == (0, 0, 0):
                if board.is_dead_end(cell.pos):
                    empty_cell_score += 10000
                else:
                    empty_cell_score += 5
    return (
        20 * distance
        - 25 * len(completedColors)
        + blocked
        + corners
        + 4 * adjacent
        + empty_cell_score)

def possiblePaths(controller):
    flag = False
    for y in range(len(controller.board_obj.height)):
        blackCount = 0
        incompleteColors = 0
        for x in range(len(controller.board_obj.width)):
            currentValue = controller.board_obj.board[x][y].value
            if currentValue == ".":
                blackCount = blackCount + 1
            for roots in controller.board_obj.paths.values():  
                pointA = roots[0][-1]
                pointB = roots[1][-1]
                #XOR to see if the end of only one path is above this line
                if (pointA.pos[1] < y) ^ (pointB.pos[1] < y):
                    incompleteColors = incompleteColors + 1




def find_stranded_colors_with_black_mask(controller):
    """
    Find stranded colors based on whether they can connect across black regions, using the paths dictionary.

    Parameters:
    board (list of list of Node): A 2D list representing the board where each element is a Node object.
    paths (dict): A dictionary where keys are color values and values are lists of paths containing Node objects.

    Returns:
    dict: A dictionary where the keys are colors (tuples) and the values are booleans indicating if the color is stranded.
    """
    board = controller.board_obj
    # Convert the board to a NumPy array of colors
    color_array = np.array([[node.value for node in row] for row in board.board])
    
    # Define black color
    black = "."
    
    # Dictionary to hold the stranded status for each color
    stranded_status = {}

    incomplete_colors = board.get_incomplete_colors()

    for color in incomplete_colors:
        # Retrieve the current and goal positions from the paths
        current_position = board.paths[color][0][-1].pos
        goal_position = board.paths[color][1][-1].pos

        # Start by creating a mask that is True for all black cells (".")
        color_mask = (color_array == ".")

        # Then, manually set the start and end positions to True
        color_mask[current_position[0], current_position[1]] = True
        color_mask[goal_position[0], goal_position[1]] = True
        
        # Label the connected regions for the current color value and black regions
        labeled_color_regions, _ = label(color_mask)
    
        # Check if both current and goal positions are in the same labeled region
        current_label = labeled_color_regions[current_position]
        goal_label = labeled_color_regions[goal_position]

        if current_label != goal_label:
            # If they are not in the same region, the color is stranded
            stranded = True
        else:
            stranded = False
        stranded_status[color] = stranded

    return stranded_status



# checks to see if the most current cell in this violates having adjacent cells of the same color
def adjacentCells(controller, path):
    count = 0
    board = controller.board_obj
    x, y = path[-1].pos
    for move in moves:
        i, j = moves[move]
        x2 = i + x
        y2 = j + y
        if board.validPos(x2, y2):
            if (
                board.board[x2][y2].value == board.board[x][y].value
                and board.board[x2][y2] != path[-2]
                and not board.board[x2][y2].root
            ):
                count = count + 1
    return count



def select_incomplete_color(controller):
    incomplete_colors = controller.board_obj.get_incomplete_colors()
    if incomplete_colors:
        color = np.random.choice(incomplete_colors)
        if len(controller.board_obj.paths[color][0]) > len(
            controller.board_obj.paths[color][1]
        ):
            return (color, 0)
        else:
            return (color, 1)
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
            # If path containing pointA has more than 1 node, only account for pointA
            if len(roots[0]) > len(roots[1]):
                if Avalue < minMoves:
                    minMoves = Avalue
                    minValue = [pointA.value, 0]
            # If path containing pointB has more than 1 node, only account for pointB
            elif len(roots[1]) > len(roots[0]):
                if Bvalue < minMoves:
                    minMoves = Bvalue
                    minValue = [pointB.value, 1]
            # If both paths have only 1 node, account for both pointA and pointB
            else:
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
    best_constraint = 5
    for move in moves:
        controller.makeDummyMove(pos, move)
        updated_score = evaluateBoard(controller)
        updated_constraint = get_available_moves(controller.board_obj, move)
        if updated_score < best_score:
            best_score = updated_score
            best_move = move
            best_constraint = updated_constraint
        if updated_score == best_score and updated_constraint <= best_constraint:
            best_score = updated_score
            best_move = move
            best_constraint = get_available_moves(controller.board_obj, move)
        controller.dummyRemove(move)
    return best_move


def delete_path(controller, delete_path, random_delete, guaranteed_paths):
    if random_delete:
        if len(delete_path) > 1:
            length = np.random.choice(range(1,len(delete_path)))
        else:
            length = 0
    else:
        length = len(delete_path)
    for i in range(length):
        if delete_path[-1].pos in guaranteed_paths:
            break
        controller.remove(delete_path[-1].pos)


def get_constraining_path(controller, path):
    node = path[-1]
    value = node.value
    x, y = node.pos
    constraining_colors = []
    constrained_path = []
    for move in moves:
        i, j = moves[move]
        if controller.board_obj.validPos(x + i, y + j):
            neighbor = controller.board_obj.board[x + i][y + j]
            constraining_colors.append(neighbor)
    if constraining_colors:
        for color in constraining_colors:
            constrained_path.append(controller.board_obj.find_node_path(color))
    return constrained_path


def find_forced_moves(controller):
    board = controller.board_obj
    forced_moves = set()
    exclude_moves = set()
    destinations = set()  # To track destination positions
    empty_space_to_paths = {}  # To track which paths lead to each empty space

    for roots in board.paths.values():
        if board.connectedPath(roots[0][0].value):
            continue
        for path in roots:
            start_pos = path[-1].pos
            available_moves = board.get_available_moves(start_pos)
            if len(available_moves) == 1:
                move = (start_pos, available_moves[0])
                forced_moves.add(move)
                destinations.add(available_moves[0])
            else:
                # Collect potential moves for the second condition
                adjacent_empty_spaces = board.get_adjacent_empty_spaces(start_pos)
                for empty_space in adjacent_empty_spaces:
                    empty_space_neighbors = board.get_available_moves(empty_space)
                    if len(empty_space_neighbors) == 1:
                        move = (start_pos, empty_space)
                        if empty_space in empty_space_to_paths:
                            empty_space_to_paths[empty_space].append(move)
                        else:
                            empty_space_to_paths[empty_space] = [move]

    # Exclude moves if an empty space is shared by two or more paths
    for empty_space, moves in empty_space_to_paths.items():
        if len(moves) > 1:
            exclude_moves.update(moves)
        else:
            move = moves[0]
            _, dest = move
            if dest not in destinations:
                forced_moves.add(move)
                destinations.add(dest)

    # Remove excluded moves from forced moves
    final_forced_moves = forced_moves - exclude_moves

    return list(final_forced_moves)


def make_forced_moves(controller):
    while True:
        forced_moves = find_forced_moves(controller)
        if not forced_moves:
            break
        for start_pos, move in forced_moves:
            controller.makeMove(start_pos, move)


def board_solver_simulated_annealing(controller):
    board = controller.board_obj

    roots = board.paths

    temperature = 200

    cooling_rate = 0.95

    guaranteed_paths = set()  # To store the guaranteed paths

    make_forced_moves(controller)
    for roots_values in board.paths.values():
        for path in roots_values:
            guaranteed_paths.add(path[0].pos)
            for node in path:
                guaranteed_paths.add(node.pos)
    counter = 0

    while temperature > 1:
        if not controller.isGameOver():
            # if counter >= 30 and completed_colors:
            #     index = np.random.choice(range(len(completed_colors)))
            #     value = completed_colors[index]
            #     delete = roots[value]
            #     delete_path(controller, delete[0], False, guaranteed_paths)
            #     delete_path(controller, delete[1], False, guaranteed_paths)
            #     completed_colors_count -= 1
            #     counter = 0

            make_forced_moves(controller)
            can_move, block_pos = board.has_possible_moves()
            # This writes a check to see if
            if not can_move:
                try:
                    constraining_paths = get_constraining_path(controller, block_pos)
                    constraining_path = random.choice(constraining_paths)
                    delete_path(controller, constraining_path, False, guaranteed_paths)
                except:
                    continue
                temperature *= 1.1
            stranded_status = find_stranded_colors_with_black_mask(controller)
            for color, stranded in stranded_status.items():
                if stranded:
                    keys = list(board.paths.keys())
                    keys.remove(color)
                    random_color = random.choice(keys)
                    delete_path(controller, board.paths[color][0], False, guaranteed_paths)
                    delete_path(controller, board.paths[color][1], False, guaranteed_paths)
                    delete_path(controller, board.paths[random_color][0], False, guaranteed_paths)
                    delete_path(controller, board.paths[random_color][1], False, guaranteed_paths)
                    temperature *= 1.3
                    temperature = min(temperature,200)
            # # This writes a check to see if


            if np.random.rand() >= 0.4:
                selected_color = mostConstrainedPath(controller)
            else:
                selected_color = select_incomplete_color(controller)

            if selected_color:
                selected_path = roots[selected_color[0]][selected_color[1]]

                available_moves = get_available_moves(
                    controller.board_obj, selected_path[-1].pos
                )
                if available_moves:
                    best_pos = get_best_available(
                        controller, selected_path[-1].pos, available_moves
                    )
                    rand_pos = random.choice(available_moves)


                    try:
                        controller.makeDummyMove(selected_path[-1].pos, best_pos)
                        best_score = evaluateBoard(controller)
                        controller.dummyRemove(best_pos)

                        controller.makeDummyMove(selected_path[-1].pos, rand_pos)
                        rand_score = evaluateBoard(controller)
                        controller.dummyRemove(rand_pos)

                        if np.random.uniform(0, 1) <= np.exp(
                            (best_score - rand_score) / temperature
                        ):
                            best_pos = rand_pos

                        controller.makeMove(selected_path[-1].pos, best_pos)
                        temperature *= cooling_rate
                    except:
                        temperature *= cooling_rate
                    counter += 1
                # print(temperature)

        else:
            return True
