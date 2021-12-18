"""
Need to implement:
13.12.21
[√]Screen
[√]Grid
[√]Input * NEED TO SAVE DATA TO SHOW ON SCREEN [√]
[√]Algorithm
[]Visualized * Working on it NOW
"""

import pygame
import time

pygame.font.init()

WIDTH = 900
HEIGHT = 900
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Auto Sudoku Solver")

WHITE = (255,255,255)
GREY = (128,128,128)
BLACK = (0,0,0)
GREEN = (0,255,0)
TURQUOISE = (64,244,208)
PINK = (255,102,255)

done = False

#Creating cell(box) object
class Box:

    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.color = WHITE
        self.value = 0
        self.options = []

    #Set value of cell
    def set_value(self,num):
        self.value = num

    def get_value(self):
        return self.value

    #Get cell position
    def get_pos(self):
        return self.row,self.col

    #draw the cell
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x, self.y, self.width, self.width))

    #Color the cell when its clicked
    def make_clicked(self):
        self.color = TURQUOISE

    #"Un-color" the cell when it was clicked again
    def make_clear(self):
        self.color = WHITE

    def is_clear(self):
        if self.color == WHITE:
            return True

    def what_color(self):
        return self.color

    #Make it colored for visuals
    def make_check_tile(self):
        self.color = PINK

    #Color cell as an option
    def make_is_option(self):
        self.color = GREY

    #Check if the cell IS clicked
    def is_clicked(self):
        return self.color

    # Draw the number on screen
    def draw_number(self,win, text, pos):
        largeText = pygame.font.Font('freesansbold.ttf', 72)
        TextSurf, TextRect = text_objects(text, largeText)
        x, y = pos
        TextRect.center = (x, y)
        win.blit(TextSurf, TextRect)

#Call to solve with a flag if done
def solve(grid,win, ROWS, width):
    global done
    to_solve = 0
    for row in grid:
        for box in row:
            if (box.get_value() == 0):
                to_solve += 1
                box.make_check_tile()
                draw(win, grid, ROWS, width)
                algorithm(grid,box, win, ROWS, width)
                time.sleep(0.01)
                box.make_clear()

    if (to_solve == 0):
        done = True

#Algorithm
def algorithm(grid,box, win, ROWS, width):
    options = []
    option = 0
    current_box = []

    for row in grid[box.row // 3 * 3:box.row // 3 * 3 + 3]:
        for box in row[box.col // 3 * 3:box.col // 3 * 3 + 3]:
            if (box.get_value() != 0):
                current_box.append(box.get_value())

    for num in range(1,10):
        for row in grid[box.row // 3 * 3:box.row // 3 * 3 + 3]:
            for box in row[box.col // 3 * 3:box.col // 3 * 3 + 3]:
                if (box.get_value() == 0 and num not in current_box):
                    if (check_horizontal(grid,box,num) is True and check_vertical(grid,box,num) is True):
                        options.append(box)
                        option = num
        if (len(options) == 1):
            options[0].set_value(option)
        else:
            options.clear()

#Checking if the number exist Horizontally
def check_horizontal(grid,cell,num):
    for row in grid:
        for box in row[cell.col:cell.col+1]:
            if (box.get_value() == num):
                return False
    return True

#Checking if the number exist veritcally
def check_vertical(grid,cell,num):
    for row in grid[cell.row:cell.row+1]:
        for box in row:
            if (box.get_value() == num):
                return False
    return True

#Create the grid
def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            box = Box(i, j, gap, rows);
            grid[i].append(box)

    return grid

#Draw the grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        if (i == 3 or i == 6):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap), width = 10)
        else:
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            if (j == 3 or j == 6):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width), width = 10)
            else:
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


#Draw everything
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for box in row:
            box.draw(win)

    draw_values(win, grid)
    draw_grid(win, rows, width)
    pygame.display.update()

#Draw values on screen
def draw_values(win, grid):
        for row in grid:
            for box in row:
                if (box.get_value() in (1,2,3,4,5,6,7,8,9)):
                    box.draw_number(win, str(box.get_value()), get_cell([box.x,box.y]))

#Get clicked position
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

#Get cell position
def get_cell(pos):
    x,y = pos

    row = x - x % 100
    col = y - y % 100
    row += 50
    col += 50

    return row,col

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def main(win,width):
    ROWS = 9
    grid = make_grid(ROWS, width)

    run = True
    tile_clicked = False

    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT Mouse Button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                box = grid[row][col]
                if (tile_clicked == False):
                    clicked = box
                    clicked.make_clicked()
                    draw(win,grid,ROWS,width)
                    tile_clicked = True
                else:
                    clicked.make_clear()
                    draw(win, grid, ROWS, width)
                    tile_clicked = False

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                box = grid[row][col]
                if (box.get_value() != 0):
                    box.set_value(0)

            if event.type == pygame.KEYDOWN and tile_clicked:
                if (event.unicode in ('1','2','3','4','5','6','7','8','9')):
                    clicked.set_value(int(event.unicode))
                if event.key == pygame.K_SPACE:
                    while (not done):
                        solve(grid,win, ROWS, width)


    pygame.quit()

main(WIN,WIDTH)
