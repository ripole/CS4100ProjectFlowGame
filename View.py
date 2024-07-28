import pygame
from GameRules import Board,test_Board


def draw_timer(screen, elapsed_time, font):
    timer_surface = font.render(f'Time Spent: {elapsed_time // 1000}', True, (0, 0, 0))
    screen.blit(timer_surface, (10, 10))


class View:

    def __init__(self, board_obj):
        self.board_obj = board_obj
        self.timer_offset = 30
        self.cell_size = 50

    def draw_board(self,screen):
        for x in range(self.board_obj.board_width):
            for y in range(self.board_obj.board_height):
                color = self.board_obj.board[x][y].color
                pygame.draw.rect(screen, color, pygame.Rect(y * self.cell_size, x * self.cell_size + self.timer_offset, self.cell_size, self.cell_size))

        # Draw the grid lines
        for x in range(self.board_obj.board_width):
            pygame.draw.line(screen, (200, 200, 200), (0, x * self.cell_size + self.timer_offset),
            (self.board_obj.board_width * self.cell_size, x * self.cell_size + self.timer_offset))
        for y in range(self.board_obj.board_height):
            pygame.draw.line(screen, (200, 200, 200), (y * self.cell_size, self.timer_offset),
                            (y * self.cell_size, self.board_obj.board_height * self.cell_size + self.timer_offset))
