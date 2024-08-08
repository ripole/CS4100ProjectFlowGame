import GameRules as modelClass
from GameRules import read_boards
import View as viewClass
import pygame
import time
from FlowSolver import board_solver_simulated_annealing
import copy


class GuiController:
    def __init__(self, filename):
        self.board_obj = modelClass.Board(read_boards(filename)[0])
        self.view = viewClass.View(self.board_obj)
        self.selected_cell = None
        self.message = ""
        self.message_time = 0
        self.message_duration = 3
        self.solver_active = False
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.sleeptime = 0.005
        self.screen_size = (
            self.board_obj.board_width * self.view.cell_size,
            self.board_obj.board_height * self.view.cell_size + self.view.timer_offset,
        )
        self.screen = pygame.display.set_mode(self.screen_size)

    def isGameOver(self):
        return self.board_obj.gameOver()

    def makeMove(self, current_pos, new_pos):
        try:
            self.board_obj.extendPath(current_pos, new_pos)
            self.message = ""
            self.refresh()
        except Exception as e:
            self.message = str(e)
            self.message_time = time.time()
            self.refresh()

    def makeDummyMove(self, current_pos, new_pos):
        try:
            self.board_obj.extendPath(current_pos, new_pos)
        except Exception as e:
            self.message = str(e)
            self.message_time = time.time()
            self.refresh()

    def remove(self, new_pos):
        try:
            self.board_obj.removeNode(new_pos)
            self.message = ""
            self.refresh()
        except Exception as e:
            self.message = str(e)
            self.message_time = time.time()
            # self.refresh()

    def dummyRemove(self, new_pos):
        try:
            self.board_obj.removeNode(new_pos)

        except Exception as e:
            self.message = str(e)
            self.message_time = time.time()
            self.refresh()

    def display_message(self, screen):
        if self.message and (time.time() - self.message_time) < self.message_duration:
            font = pygame.font.Font("freesansbold.ttf", 19)
            text = font.render(
                self.message, True, (255, 0, 0)
            )  # Red color for error message
            screen.blit(
                text, (10, self.board_obj.board_height * self.view.cell_size + 5)
            )

    def handle_click(self, pos):
        y, x = pos
        x -= self.view.timer_offset
        if x < 0:  # If the click is within the timer area, ignore it
            return
        grid_x = x // self.view.cell_size
        grid_y = y // self.view.cell_size
        if self.selected_cell:
            self.makeMove(self.selected_cell, (grid_x, grid_y))
            self.selected_cell = None
        else:
            self.selected_cell = (grid_x, grid_y)

    def refresh(self):
        self.screen.fill((255, 255, 255))
        self.view.draw_board(self.screen)
        elapsed_time = pygame.time.get_ticks()
        viewClass.draw_timer(
            self.screen, elapsed_time, pygame.font.Font("freesansbold.ttf", 19)
        )
        self.display_message(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)
        time.sleep(self.sleeptime)

    def run(self):
        pygame.init()
        pygame.display.set_caption("Flow Game")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.solver_active = not self.solver_active
            self.refresh()
            if self.solver_active:
                board_solver_simulated_annealing(self)
                self.solver_active = False
        pygame.quit()


class NoGuiController:
    def __init__(self, filename):
        self.board_obj = modelClass.Board(read_boards(filename)[40])

    def isGameOver(self):
        return self.board_obj.gameOver()

    def makeMove(self, current_pos, new_pos):
        try:
            self.board_obj.extendPath(current_pos, new_pos)
        except Exception as e:
            print(e)

    def makeDummyMove(self, current_pos, new_pos):
        try:
            self.board_obj.extendPath(current_pos, new_pos)
        except Exception as e:
            print(e)

    def remove(self, new_pos):
        try:
            self.board_obj.removeNode(new_pos)
        except Exception as e:
            print(e)

    def dummyRemove(self, new_pos):
        try:
            self.board_obj.removeNode(new_pos)
        except Exception as e:
            print(e)

    def run(self):
        board_solver_simulated_annealing(self)


 


controller = GuiController("Puzzles/janko.txt")
controller.run()
