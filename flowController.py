import GameRules as modelClass
from GameRules import read_boards
import View as viewClass
import pygame
import time
from FlowSolver import board_solver_simulated_annealing
import copy


class BaseController:
    def __init__(self, filename):
        board_configs = read_boards(filename)
        self.boards = [modelClass.Board(config) for config in board_configs]
        self.current_board_index = 64
        self.board_obj = self.boards[self.current_board_index]
        self.message = ""

    def set_current_board(self, index):
        """Set the current board to the one at the specified index in the list."""
        if 0 <= index < len(self.boards):
            self.current_board_index = index
            self.board_obj = self.boards[self.current_board_index]
        else:
            raise IndexError("Board index out of range.")

    def isGameOver(self):
        return self.board_obj.gameOver()

    def makeMove(self, current_pos, new_pos):
        try:
            self.board_obj.extendPath(current_pos, new_pos)
            self.message = ""
            self.refresh()
        except Exception as e:
            self.message = str(e)
            self.handle_error()

    def makeDummyMove(self, current_pos, new_pos):
        try:
            self.board_obj.extendPath(current_pos, new_pos)
        except Exception as e:
            self.message = str(e)
            self.handle_error()

    def remove(self, new_pos):
        try:
            self.board_obj.removeNode(new_pos)
            self.message = ""
            self.refresh()
        except Exception as e:
            self.message = str(e)
            self.handle_error()

    def dummyRemove(self, new_pos):
        try:
            self.board_obj.removeNode(new_pos)
        except Exception as e:
            self.message = str(e)
            self.handle_error()

    def handle_error(self):
        """Override this method in child classes to handle errors."""
        pass

    def refresh(self):
        """Override this method in child classes to refresh the display or state."""
        pass

    def run(self):
        """Override this method in child classes to define the main loop."""
        pass


class GuiController(BaseController):
    def __init__(self, filename):
        super().__init__(filename)
        self.view = viewClass.View(self.board_obj)
        self.selected_cell = None
        self.message_time = 0
        self.message_duration = 1
        self.solver_active = False
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.sleeptime = 0.005
        self.screen_size = (
            self.board_obj.board_width * self.view.cell_size,
            self.board_obj.board_height * self.view.cell_size + self.view.timer_offset,
        )
        self.screen = pygame.display.set_mode(self.screen_size)
        self.start_time = pygame.time.get_ticks()

    def set_current_board(self, index):
            """Set the current board to the one at the specified index in the list."""
            if 0 <= index < len(self.boards):
                self.current_board_index = index
                self.board_obj = self.boards[self.current_board_index]
                self.view = viewClass.View(self.board_obj)
                self.screen_size = (
                self.board_obj.board_width * self.view.cell_size,
                self.board_obj.board_height * self.view.cell_size + self.view.timer_offset,
                )        
                self.screen = pygame.display.set_mode(self.screen_size)
                self.start_time = pygame.time.get_ticks()
            else:
                raise IndexError("Board index out of range.")

    def handle_error(self):
        self.message_time = time.time()
        self.refresh()

    def refresh(self):
        self.screen.fill((255, 255, 255))
        self.view.draw_board(self.screen)
        elapsed_time = pygame.time.get_ticks() - self.start_time
        viewClass.draw_timer(
            self.screen, elapsed_time, self.current_board_index + 1, pygame.font.Font("freesansbold.ttf", 19)
        )
        self.display_message()
        pygame.display.flip()
        self.clock.tick(self.fps)
        time.sleep(self.sleeptime)

    def display_message(self):
        if self.message and (time.time() - self.message_time) < self.message_duration:
            font = pygame.font.Font("freesansbold.ttf", 19)
            text = font.render(self.message, True, (255, 0, 0))  # Red color for error message
            self.screen.blit(text, (10, self.board_obj.board_height * self.view.cell_size + 5))

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
                time.sleep(3)
                self.set_current_board(self.current_board_index + 1)
        pygame.quit()


class NoGuiController(BaseController):
    def handle_error(self):
        # print(self.message)
        pass
    def refresh(self):
        pass  # No GUI, so no refresh needed

    def run(self):
        while self.current_board_index < len(self.boards):
            start_time = time.time()
            board_solver_simulated_annealing(self)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Completed Board: {self.current_board_index} in {elapsed_time:.2f} seconds")
            self.set_current_board(self.current_board_index + 1)



 


controller = GuiController("Puzzles/janko.txt")
controller.run()
