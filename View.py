import pygame
from GameRules import Board
from ParseBoard import read_boards

boards = read_boards("Puzzles/8by8Puzzles.txt")
board = boards[1]

def draw_board(screen, board, cell_size, y_offset):
    for x in range(len(board.board)):
        for y in range(len(board.board[0])):
            color = board.board[x][y].color
            pygame.draw.rect(screen, color, pygame.Rect(y * cell_size, x * cell_size + y_offset, cell_size, cell_size))
    
    # Draw the grid lines
    for x in range(len(board.board) + 1):
        pygame.draw.line(screen, (200, 200, 200), (0, x * cell_size + y_offset), (len(board.board[0]) * cell_size, x * cell_size + y_offset))
    for y in range(len(board.board[0]) + 1):
        pygame.draw.line(screen, (200, 200, 200), (y * cell_size, y_offset), (y * cell_size, len(board.board) * cell_size + y_offset))

def draw_timer(screen, elapsed_time, font):
    timer_surface = font.render(f'Time Spent: {elapsed_time // 1000}', True, (0, 0, 0))
    screen.blit(timer_surface, (10, 10))



pygame.init()
timer_offset = 30
cell_size = 50
board_width = len(board)
board_height = len(board[0])
screen_size = (board_width * cell_size, board_height * cell_size+timer_offset)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Flow Game")
clock = pygame.time.Clock()
board_obj = Board(board)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # White background
    draw_board(screen, board_obj, cell_size,timer_offset)
    elapsed_time = pygame.time.get_ticks()
    draw_timer(screen, elapsed_time, pygame.font.Font('freesansbold.ttf',19))

    pygame.display.flip()
    clock.tick(30)  # FPS

pygame.quit()
