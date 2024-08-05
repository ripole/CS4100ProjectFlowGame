import numpy as np
import copy
def evaluateBoard(controller):
    board = controller.board_obj
    cornerList = [[0,0], [0,len(board.board)-1], [len(board.board[0])-1, 0],[len(board.board[0])-1, len(board.board)-1]]
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
            Ax,Ay = pointA.pos
            Bx,By = pointB.pos
            distance += abs(Ax - Bx) + abs(Ay - By)
            if len(get_available_moves(board, pointA.pos)) == 0 or len(get_available_moves(board, pointB.pos)) == 0:
                blocked = 1000
        for coords in cornerList:
            if get_available_moves(board, coords) is None:
                corners = corners + 10
    empty_cell_score = 0
    for row in board.board:
        for cell in row:
            if cell.color == (0, 0, 0):
                empty_cell_score += 5
            
    return  distance - len(completedColors) + blocked + corners + empty_cell_score,completedColors

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

def get_best_available(controller,pos,moves):
    best_score = 10000000
    best_move = moves[np.random.choice(range(len(moves)))]
    if np.random.uniform(0, 1) < .1:
        return best_move
    else:
        for move in moves:
            controller.makeDummyMove(pos,move)
            updated_score,completed_colors = evaluateBoard(controller)
            if updated_score <= best_score:
                best_score = updated_score
                best_move = move
            controller.dummyRemove(move)
        return best_move

def delete_path(controller,delete_path,random):
    if random:
        length = np.random.choice(range(len(delete_path)))
    else:
        length = len(delete_path)-1
    for i in range(length):
            controller.remove(delete_path[-1].pos)


def board_solver_simulated_annealing(controller):
    board = controller.board_obj

    roots = board.paths


    temperature = 100

    cooling_rate = .9

    current_score,completed_colors = evaluateBoard(controller)

    counter = 0

    completed_colors_count = 0
    

    while temperature > 1:

        if counter >= 20 and completed_colors:
            index = np.random.choice(range(len(completed_colors)))
            value = completed_colors[index]
            delete = roots[value][0]
            delete_path(controller,delete,False)
            completed_colors_count -= 1
            counter = 0

        
        selected_color = select_incomplete_color(controller,completed_colors)

        if selected_color != None:
            selected_path = roots[selected_color][0]

            available_moves = get_available_moves(controller.board_obj, selected_path[-1].pos)
           

            new_pos = get_best_available(controller,selected_path[-1].pos,available_moves)

            try:
                controller.makeMove(selected_path[-1].pos, new_pos)
                updated_score,completed_colors = evaluateBoard(controller)
                print(completed_colors_count,len(completed_colors))

                if completed_colors_count < len(completed_colors):
                    completed_colors_count += 1
                    counter = 0

                if updated_score < current_score or np.random.uniform(0, 1) <= np.exp((current_score - updated_score) / temperature):
                    current_score = updated_score
                else:
                    available_moves = get_available_moves(controller.board_obj, new_pos)
                    controller.remove(new_pos)
                    if not available_moves:
                        if not selected_path[-1].root:
                            delete_path(controller,selected_path,True)
                temperature *= cooling_rate
            except:
                temperature *= cooling_rate
            counter += 1

        else:
            break


