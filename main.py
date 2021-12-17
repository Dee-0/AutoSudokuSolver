"""
Need to implement:
13.12.21
[√]Screen
[√]Grid
[√]Input * NEED TO SAVE DATA TO SHOW ON SCREEN [√]
[]Algorithm * Working on it NOW
[]Visualized
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

def draw_values(win, grid):
        for row in grid:
            for box in row:
                if (box.get_value() in (1,2,3,4,5,6,7,8,9,)):
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

            if event.type == pygame.KEYDOWN and tile_clicked:
                clicked.set_value(int(event.unicode))


    pygame.quit()

main(WIN,WIDTH)




#Junk that was tested

"""#Receieve pressed number
def get_inserted_number(key):
    print(key)
    event_key = key
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.event_key:
                print("hi")"""