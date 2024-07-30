import GameRules as modelClass
from GameRules import read_boards
import View as viewClass
import pygame
import time


class Player:
    def __init__(self, controller):
        self.controller = controller
        self.moves = [
            (1, 1, 1, 2),
            (1, 2, 1, 3),
            (1, 3, 1, 4),
        ]
        self.current_move_index = 0

    def get_next_move(self):
        if self.current_move_index < len(self.moves):
            move = self.moves[self.current_move_index]
            self.current_move_index += 1
            return move
        return None


class Controller:
    def __init__(self, filename):
        self.board_obj = modelClass.Board(read_boards(filename)[0])
        self.view = viewClass.View(self.board_obj)
        self.timer_offset = 30
        self.cell_size = 50
        self.selected_cell = None
        self.message = ""
        self.message_time = 0
        self.message_duration = 4
        self.agent_active = True
        self.player = Player(self)

    def isGameOver(self):
        return self.board_obj.gameOver()

    def makeMove(self, x, y, i, j):
        try:
            self.board_obj.extendPath(x, y, i, j)
            self.message = ""
        except Exception as e:
            self.message = str(e)
            self.message_time = time.time()

    def display_message(self, screen):
        if self.message and (time.time() - self.message_time) < self.message_duration:
            font = pygame.font.Font('freesansbold.ttf', 19)
            text = font.render(self.message, True, (255, 0, 0))  # Red color for error message
            screen.blit(text, (10, self.board_obj.board_height * self.cell_size + 5))

    def handle_click(self, pos):
        x, y = pos
        y -= self.timer_offset
        if y < 0:  # If the click is within the timer area, ignore it
            return
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        if self.selected_cell:
            prev_x, prev_y = self.selected_cell
            self.makeMove(prev_x, prev_y, grid_x, grid_y)
            self.selected_cell = None
        else:
            self.selected_cell = (grid_x, grid_y)

    def agent_move(self):
        move = self.player.get_next_move()
        if move:
            x, y, i, j = move
            self.makeMove(x, y, i, j)
        else:
            self.agent_active = False

    def run(self):
        pygame.init()
        pygame.display.set_caption("Flow Game")
        screen_size = (
            self.board_obj.board_width * self.cell_size,
            self.board_obj.board_height * self.cell_size + self.timer_offset)
        screen = pygame.display.set_mode(screen_size)
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
            screen.fill((255, 255, 255))  # White background
            if self.agent_active:
                self.agent_move()
                time.sleep(1)
            self.view.draw_board(screen)
            elapsed_time = pygame.time.get_ticks()
            viewClass.draw_timer(screen, elapsed_time, pygame.font.Font('freesansbold.ttf', 19))
            self.display_message(screen)

            pygame.display.flip()
            clock.tick(30)  # FPS

        pygame.quit()


controller = Controller("Puzzles/8by8Puzzles.txt")
controller.run()
