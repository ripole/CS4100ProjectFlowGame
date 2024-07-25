import pygame
from GameRules import Board
from ParseBoard import read_boards

boards = read_boards("Puzzles/8by8Puzzles.txt")
board = boards[1]
board_obj = Board(board)

class View:

    def __init__(self, board_obj):
        self.board_obj = board_obj
        self.timer_offset = 30
        self.cell_size = 50
        self.board_width = len(board)
        self.board_height = len(board[0])

    def draw_timer(self,screen, elapsed_time, font):
        timer_surface = font.render(f'Time Spent: {elapsed_time // 1000}', True, (0, 0, 0))
        screen.blit(timer_surface, (10, 10))

    def draw_board(self,screen):
        for x in range(len(board_obj.board)):
            for y in range(len(board_obj.board[0])):
                color = board_obj.board[x][y].color
                pygame.draw.rect(screen, color, pygame.Rect(y * self.cell_size, x * self.cell_size + self.timer_offset, self.cell_size, self.cell_size))

        # Draw the grid lines
        for x in range(len(self.board_obj.board) + 1):
            pygame.draw.line(screen, (200, 200, 200), (0, x * self.cell_size + self.timer_offset),
                            (len(self.board_obj.board) * self.cell_size, x * self.cell_size + self.timer_offset))
        for y in range(len(self.board_obj.board[0]) + 1):
            pygame.draw.line(screen, (200, 200, 200), (y * self.cell_size, self.timer_offset),
                            (y * self.cell_size, len(self.board_obj.board) * self.cell_size + self.timer_offset))
    def run(self):
        pygame.init()
        pygame.display.set_caption("Flow Game")
        screen_size = (self.board_width * self.cell_size, self.board_height * self.cell_size + self.timer_offset)
        screen = pygame.display.set_mode(screen_size)
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))  # White background
            self.draw_board(screen)
            elapsed_time = pygame.time.get_ticks()
            self.draw_timer(screen, elapsed_time, pygame.font.Font('freesansbold.ttf', 19))

            pygame.display.flip()
            clock.tick(30)  # FPS

        pygame.quit()

testView = View(board_obj=board_obj)
testView.run()