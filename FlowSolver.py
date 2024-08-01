import numpy as np

def evaluateBoard(controller):
    completedColors = []
    distance = 0
    for roots in controller.board_obj.paths.values():
        if controller.board_obj.connectedPath(roots[0][0].value):
            completedColors.append(roots[0][0].value)
        else:
            pointA = roots[0][-1]
            pointB = roots[1][-1]
            Ax,Ay = pointA.pos
            Bx,By = pointB.pos
            distance += abs(Ax - Bx) + abs(Ay - By)
    return  distance + len(completedColors),completedColors

def select_incomplete_color(controller, completedColors):
    all_colors = list(controller.board_obj.paths.keys())
    incomplete_colors = [color for color in all_colors if color not in completedColors]
    if incomplete_colors:
        return np.random.choice(incomplete_colors)
    else:
        return None  # All colors are complete
    
def get_available_moves(board, pos):
    moves = {
        0: (-1, 0),  # up
        1: (1, 0),  # down
        2: (0, -1),  # left
        3: (0, 1)  # right
    }
    
    available_moves = []
    x, y = pos
    for move in moves.values():
        new_x, new_y = x + move[0], y + move[1]
        if board.validPos(new_x, new_y):
            neighbor_color = board.board[new_x][new_y].color
            if neighbor_color == (0, 0, 0):
                available_moves.append((new_x, new_y))
    return available_moves


def board_solver_simulated_annealing(controller):
    board = controller.board_obj

    roots = board.paths


    temperature = 100

    cooling_rate = .99

    current_score,completed_colors = evaluateBoard(controller)


    while temperature > 1:
        
        selected_color = select_incomplete_color(controller,completed_colors)

        if selected_color != None:
            selected_path = roots[selected_color][0]

            available_moves = get_available_moves(controller.board_obj, selected_path[-1].pos)
            
            if not available_moves:
                if not selected_path[-1].root:
                    for i in range(np.random.choice(range(len(selected_path)))):
                        controller.remove(selected_path[-1].pos)
                temperature *= cooling_rate
                continue

            new_pos_index = np.random.choice(range(len(available_moves)))
            new_pos = available_moves[new_pos_index]

            try:
                controller.makeMove(selected_path[-1].pos, new_pos)
                updated_score,completed_colors = evaluateBoard(controller)

                if updated_score < current_score or np.random.uniform(0, 1) <= np.exp((current_score - updated_score) / temperature):
                    current_score = updated_score
                else:
                    controller.remove(new_pos)
                temperature *= cooling_rate
            except:
                temperature *= cooling_rate

        else:
            break


