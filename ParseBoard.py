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

# boards = read_boards('Puzzles/8by8Puzzles.txt')
# for board in boards:
#     for row in board:
#         print(''.join(row))
#     print()
#     print(board)
#     print()
