import numpy as np
import pygame
import time
from GameRules import Board,test_Board


def draw_timer(screen, elapsed_time, board_ind, font):
    timer_surface = font.render(f'Time Spent: {elapsed_time // 1000} on Board Number {board_ind}', True, (0, 0, 0))
    screen.blit(timer_surface, (10, 10))


class View:
    gridSize = 6
    cellSize = 50
    screenSize = gridSize * cellSize
    fps = 60
    sleeptime = 0.1
    black = (0, 0, 0)
    white = (255, 255, 255)
    screen = None
    clock = None
    grid = None
    def __init__(self, board_obj):
        self.board_obj = board_obj
        self.timer_offset = 30
        self.cell_size = 50

    def draw_board(self,screen):
        """Draw the board on the screen, including the grid, cell colors, and special path highlights."""
        # Loop through each cell in the board and draw the corresponding rectangle
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
        # Draw the black outline around the last node of each path
        for paths in self.board_obj.paths.values():
            for path in paths:
                # Get the last node in the path
                last_node = path[-1]  
                x, y = last_node.pos
                color = last_node.color
                # Get the root node in the path
                root_node = path[0]  
                rx, ry = root_node.pos
                center_x = ry * self.cell_size + self.cell_size // 2
                center_y = rx * self.cell_size + self.timer_offset + self.cell_size // 2
                # Create a darker shade of the color
                darker_color = tuple(max(c // 2, 0) for c in color)  
                pygame.draw.circle(screen, darker_color,(center_x,center_y), self.cell_size // 2)
                # If the path has more than one node, draw a rectangle around the last node
                if len(path) > 1:
                    pygame.draw.rect(screen, darker_color, pygame.Rect(y * self.cell_size, x * self.cell_size + self.timer_offset, self.cell_size, self.cell_size), 5)

    def drawGrid(self):
        """Draw a grid on the screen based on the cell size and screen size."""
         # Loop over the screen width
        for x in range(0, self.screenSize, self.cellSize):
            # Loop over the screen height
            for y in range(0, self.screenSize, self.cellSize):
                # Draw the rectangle on the screen with a black border for grid
                rect = pygame.Rect(x, y, self.cellSize, self.cellSize)
                pygame.draw.rect(self.screen,self.black, rect, 1)
    