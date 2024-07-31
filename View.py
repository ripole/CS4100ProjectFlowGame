import numpy as np
import pygame
import time
from GameRules import Board,test_Board


def draw_timer(screen, elapsed_time, font):
    timer_surface = font.render(f'Time Spent: {elapsed_time // 1000}', True, (0, 0, 0))
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

    def drawGrid(self):
        for x in range(0, self.screenSize, self.cellSize):
            for y in range(0, self.screenSize, self.cellSize):
                rect = pygame.Rect(x, y, self.cellSize, self.cellSize)
                pygame.draw.rect(self.screen,self.black, rect, 1)
    '''
    def setup(self,GUI=True, render_delay_sec=0.1, gs=6):
        self.gridSize = gs
        self.sleeptime = render_delay_sec
        self.grid = np.full((self.gridSize, self.gridSize), -1)


        if GUI:
            pygame.init()
            self.screenSize = self.gridSize * self.cellSize # calculate screenSize
            self.screen = pygame.display.set_mode((self.screenSize, self.screenSize))
            pygame.display.set_caption("Shape Placement Grid")
            self.clock = pygame.time.Clock()

            self.refresh()

    def refresh(self):
        self.screen.fill(self.white)
        self.drawGrid()
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.grid[i, j] != -1:
                    rect = pygame.Rect(j * self.cellSize, i * self.cellSize, self.cellSize, self.cellSize)
                    pygame.draw.rect(self.screen, self.colors[grid[i, j]], rect)

        drawShape(screen, shapes[currentShapeIndex], colors[currentColorIndex], shapePos)

        pygame.display.flip()
        self.clock.tick(self.fps)
        self.time.sleep(self.sleeptime)

    def loop_gui(self):
        running = True
        while running:
            self.screen.fill(self.white)
            self.drawGrid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                #TODO: edit this to correspond to the correct changes on the board
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        shapePos[1] = max(0, shapePos[1] - 1)
                    elif event.key == pygame.K_s:
                        shapePos[1] = min(gridSize - len(shapes[currentShapeIndex]), shapePos[1] + 1)
                    elif event.key == pygame.K_a:
                        shapePos[0] = max(0, shapePos[0] - 1)
                    elif event.key == pygame.K_d:
                        shapePos[0] = min(gridSize - len(shapes[currentShapeIndex][0]), shapePos[0] + 1)
                    elif event.key == pygame.K_p:
                        if canPlace(grid, shapes[currentShapeIndex], shapePos):
                            placeShape(grid, shapes[currentShapeIndex], shapePos, currentColorIndex)
                            placedShapes.append((currentShapeIndex, shapePos.copy(), currentColorIndex))
                            if checkGrid(grid):
                                print("All cells are covered with no overlaps and no adjacent same colors!")
                            else:
                                print("Grid conditions not met!")
                    elif event.key == pygame.K_h:
                        currentShapeIndex = (currentShapeIndex + 1) % len(shapes)
                        print("Current shape", shapesIdxToName[currentShapeIndex])
                    elif event.key == pygame.K_k:
                        currentColorIndex = (currentColorIndex + 1) % len(colors)
                    elif event.key == pygame.K_u:  # Undo the last placed shape
                        if placedShapes:
                            lastShapeIndex, lastShapePos, lastColorIndex = placedShapes.pop()
                            removeShape(grid, shapes[lastShapeIndex], lastShapePos)
                    elif event.key == pygame.K_e:  # Export the grid state
                        gridState = exportGridState(grid)
                        print("Exported Grid State:", gridState)
                        print("Placed Shapes:", placedShapes)
                    elif event.key == pygame.K_i:  # Import the grid state, not needed for us.
                        # Dummy grid state for testing
                        dummyGridState = exportGridState(np.random.randint(-1, 4, size=(gridSize, gridSize)))
                        grid = importGridState(dummyGridState)
                        placedShapes.clear()  # Clear history since we are importing a new state

            # Draw already placed shapes
            for i in range(self.gridSize):
                for j in range(self.gridSize):
                    if self.grid[i, j] != -1:
                        rect = pygame.Rect(j * self.cellSize, i * self.cellSize, self.cellSize, self.cellSize)
                        pygame.draw.rect(self.screen, self.colors[grid[i, j]], rect)

            drawShape(screen, shapes[currentShapeIndex], colors[currentColorIndex], shapePos)

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
    
    def execute(self, command='e'):
        #print("Enter commands (W/A/S/D to move, P to place, Q to quit, U to undo, H to change shape, K to change color):")
        # running = True
        done = False
        if command == 'E' or command == 'e' or command=='export':
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='e', key=ord('e'))
            try:
                pygame.event.post(new_event)
                self.refresh()
            except:
                pass
            return grid, placedShapes, done
        # while running:
        #     command = input("Command: ").strip().upper()
        #     if command == 'Q':
        #         running = False
        if command == 'W' or command == 'w' or command.lower() == "up":
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='w', key=ord('w'))
            try:
                pygame.event.post(new_event)
                self.refresh()
            except:
                pass
            shapePos[1] = max(0, shapePos[1] - 1)
        elif command == 'S' or command == 's' or command.lower() == "down":
            shapePos[1] = min(gridSize - len(shapes[currentShapeIndex]), shapePos[1] + 1)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='s', key=ord('s'))
            try:
                pygame.event.post(new_event)
                refresh()
            except:
                pass
        elif command == 'A' or command == 'a' or command.lower() == "left":
            shapePos[0] = max(0, shapePos[0] - 1)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='a', key=ord('a'))
            try:
                pygame.event.post(new_event)
                refresh()
            except:
                pass
        elif command == 'D' or command == 'd' or command.lower() == "right":
            shapePos[0] = min(gridSize - len(shapes[currentShapeIndex][0]), shapePos[0] + 1)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='d', key=ord('d'))
            try:
                pygame.event.post(new_event)
                refresh()
            except:
                pass
        elif command == 'P' or command == 'p' or command.lower() == "place":
            if canPlace(grid, shapes[currentShapeIndex], shapePos):
                placeShape(grid, shapes[currentShapeIndex], shapePos, currentColorIndex)
                placedShapes.append((currentShapeIndex, shapePos.copy(), currentColorIndex))
                exportGridState(grid)
                new_event = pygame.event.Event(pygame.KEYDOWN, unicode='p', key=ord('p'))
                try:
                    pygame.event.post(new_event)
                    refresh()
                except:
                    pass
                if checkGrid(grid):
                    #print("All cells are covered with no overlaps and no adjacent same colors!")
                    done = True
                else:
                    #print("Grid conditions not met!")
                    done = False
        elif command == 'H' or command == 'h' or command.lower() == "switchshape":
            currentShapeIndex = (currentShapeIndex + 1) % len(shapes)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='h', key=ord('h'))
            try:
                pygame.event.post(new_event)
                refresh()
            except:
                pass
            #print("Current shape", shapesIdxToName[currentShapeIndex])
        elif command == 'K' or command == 'k' or command.lower() == "switchcolor":
            currentColorIndex = (currentColorIndex + 1) % len(colors)
            new_event = pygame.event.Event(pygame.KEYDOWN, unicode='k', key=ord('k'))
            try:
                pygame.event.post(new_event)
                refresh()
            except:
                pass
        elif command == 'U' or command == 'u' or command.lower() == "undo":  # Undo the last placed shape
            if placedShapes:
                lastShapeIndex, lastShapePos, lastColorIndex = placedShapes.pop()
                removeShape(grid, shapes[lastShapeIndex], lastShapePos)
                new_event = pygame.event.Event(pygame.KEYDOWN, unicode='u', key=ord('u'))
                try:
                    pygame.event.post(new_event)
                    refresh()
                except:
                    pass
    
        # Display grid state
        return grid, placedShapes, done
    
    def run(self):
        #print("Select mode: 1 for GUI, 2 for Terminal")
        #mode = input("Mode: ").strip()
        self.setup(True, render_delay_sec=0.1, gs=6)
        self.loop_gui()
        # if mode == '1':
        #     loop_gui()
        # elif mode == '2':
        #     execute()'''
