import GameRules as modelClass
from GameRules import read_boards
import View as viewClass
import pygame
import time
from FlowSolver import board_solver_simulated_annealing
import pandas as pd


# There are two controllers in the class where you can run the game
# The Gui controller which will have the agent start running when you click
# The button s and will cycle through the boards and the no gui controller
# which will just run through the boards each board run three times and it
# will display the time it took and completion percentage average it took
# to run the board.
class BaseController:
    def __init__(self, filename):
        """Initialize the controller with boards from the given file."""
        board_configs = read_boards(filename)
        self.boards = [modelClass.Board(config) for config in board_configs]
        self.current_board_index = 0
        self.board_obj = self.boards[self.current_board_index]
        self.message = ""

    def set_current_board(self, index):
        """Set the current board to the one at the specified index in the list."""
        if 0 <= index < len(self.boards)-1:
            self.current_board_index = index
            self.board_obj = self.boards[self.current_board_index]
        else:
            raise IndexError("Board index out of range.")

    def isGameOver(self):
        """Check if the current game board is completed."""
        return self.board_obj.gameOver()

    def makeMove(self, current_pos, new_pos):
        """Attempt to extend the path from current_pos to new_pos on the board."""
        try:
            self.board_obj.extendPath(current_pos, new_pos)
            self.message = ""
            self.refresh()
        except Exception as e:
            self.message = str(e)
            self.handle_error()

    def makeDummyMove(self, current_pos, new_pos):
        """Make a move without refreshing or handling errors (for internal logic)."""
        try:
            self.board_obj.extendPath(current_pos, new_pos)
        except Exception as e:
            self.message = str(e)
            self.handle_error()

    def remove(self, new_pos):
        """Attempt to remove a node from the path at new_pos on the board."""
        try:
            self.board_obj.removeNode(new_pos)
            self.message = ""
            self.refresh()
        except Exception as e:
            self.message = str(e)
            self.handle_error()

    def dummyRemove(self, new_pos):
        """Remove a node without refreshing or handling errors (for internal logic)."""
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
    """Initialize the GUI controller with the specified board file."""
    def __init__(self, filename):
        super().__init__(filename)
        # Initialize the view for the current board
        self.view = viewClass.View(self.board_obj)
        # Handling clicking
        self.selected_cell = None
        # Displaying Solver
        self.message_time = 0
        self.message_duration = 1
        self.solver_active = False
        # Speed and Time of the Board
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.sleeptime = 0.005
        self.start_time = pygame.time.get_ticks()
        # Create screen to display
        self.screen_size = (
            self.board_obj.board_width * self.view.cell_size,
            self.board_obj.board_height * self.view.cell_size + self.view.timer_offset,
        )
        self.screen = pygame.display.set_mode(self.screen_size)


    def set_current_board(self, index):
            """Set the current board to the one at the specified index in the list."""
            if 0 <= index < len(self.boards):
                self.current_board_index = index
                self.board_obj = self.boards[self.current_board_index]
                # Update the view for the new board
                self.view = viewClass.View(self.board_obj)
                # Update time and screen of the GUI
                self.screen_size = (
                self.board_obj.board_width * self.view.cell_size,
                self.board_obj.board_height * self.view.cell_size + self.view.timer_offset,
                )        
                self.screen = pygame.display.set_mode(self.screen_size)
                self.start_time = pygame.time.get_ticks()
            else:
                raise IndexError("Board index out of range.")

    def handle_error(self):
        """Handle errors by displaying an error message."""
        self.message_time = time.time()
        self.refresh()

    def refresh(self):
        """Refresh the game display."""
        # Fill the screen with white
        self.screen.fill((255, 255, 255))
        # Draw the board
        self.view.draw_board(self.screen)
        # Add timer and Board index to top of screen
        elapsed_time = pygame.time.get_ticks() - self.start_time
        viewClass.draw_timer(
            self.screen, elapsed_time, self.current_board_index + 1, pygame.font.Font("freesansbold.ttf", 19)
        )
        self.display_message()
        pygame.display.flip()
        self.clock.tick(self.fps)
        time.sleep(self.sleeptime)

    def display_message(self):
        """Display the current error message if it's still within the display duration."""
        if self.message and (time.time() - self.message_time) < self.message_duration:
            font = pygame.font.Font("freesansbold.ttf", 19)
            text = font.render(self.message, True, (255, 0, 0))  # Red color for error message
            self.screen.blit(text, (10, self.board_obj.board_height * self.view.cell_size + 5))

    def handle_click(self, pos):
        """Handle mouse clicks on the board."""
        y, x = pos
        # Adjust for the timer area
        x -= self.view.timer_offset
        if x < 0:  # If the click is within the timer area, ignore it
            return
        # Calculate grid x,y-coordinate
        grid_x = x // self.view.cell_size
        grid_y = y // self.view.cell_size
        # Make a move if a cell is selected or select a cell if not
        if self.selected_cell:
            self.makeMove(self.selected_cell, (grid_x, grid_y))
            self.selected_cell = None
        else:
            self.selected_cell = (grid_x, grid_y)

    def run(self):
        """Main loop for running the GUI."""
        pygame.init()
        pygame.display.set_caption("Flow Game")
        running = True
        while running:
            for event in pygame.event.get():
                # Handle window close event
                if event.type == pygame.QUIT:
                    running = False
                # Handle mouse click event
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                # Handle Start (s) key event
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.solver_active = not self.solver_active
            # Refresh the board to display
            self.refresh()
            # Check if the solve button has been pressed 
            if self.solver_active:
                # Run agent to solve board
                board_solver_simulated_annealing(self)
                time.sleep(3)
                # Once board complete go to next board
                self.set_current_board(self.current_board_index + 1)
        pygame.quit()


class NoGuiController(BaseController):
    def handle_error(self):
        """Handle errors (no operation in NoGuiController)."""
        pass
    def refresh(self):
        """No refresh needed for NoGuiController."""
        pass 

    def run(self):
        """Run the solver and collect data for multiple boards without GUI."""
        data = []
        while self.current_board_index < 70:
            elapsed_times = []
            completion_percentages = []
            # Run each board 3 times and average results
            for _ in range(3): 
                start_time = time.time()
                board_solver_simulated_annealing(self)
                end_time = time.time()
                elapsed_time = end_time - start_time
                elapsed_times.append(elapsed_time)
                completion_percentages.append(self.board_obj.percentComplete() * 100)
                for value in self.board_obj.paths:
                    paths = self.board_obj.paths[value]
                    for path in paths:
                        for i in range(len(path)-1):
                            self.dummyRemove(path[-1].pos)
            # Calculate averages
            avg_elapsed_time = sum(elapsed_times) / len(elapsed_times)
            avg_completion_percentage = sum(completion_percentages) / len(completion_percentages)
            
            # Collect data for the current board
            board_info = {
                "Board Index": self.current_board_index,
                "Board Size": f"{self.board_obj.board_height} x {self.board_obj.board_width}",
                "Average Elapsed Time (seconds)": round(avg_elapsed_time, 2),
                "Average Percent Complete": round(avg_completion_percentage, 2)
            }
            data.append(board_info)
            
            # Print the status
            print(f"Completed Board {self.current_board_index} of Size {self.board_obj.board_height} x {self.board_obj.board_width}: " +
                  f"Average in {avg_elapsed_time:.2f} seconds and {round(avg_completion_percentage, 2)} percent complete")
            
            self.set_current_board(self.current_board_index + 1)

        # Convert the collected data to a DataFrame and export to CSV
        df = pd.DataFrame(data)
        file_name = "board_completion_data.csv"
        df.to_csv(file_name, index=False)



 


controller = GuiController("Puzzles/janko.txt")
controller.run()
