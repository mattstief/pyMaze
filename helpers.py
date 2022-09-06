from typing import List
from PIL import Image
import random
from array import *
from helpers import *
import sys
import os

#customizable values
w, h = 30, 30       #width and height of maze in #cells - 9px per cell
dir_path = "gifs/"  #relative dir to save gif
name_prefix = "maze"#name prefix - numbers are appended to file names to prevent overwriting - maze0.gif, maze1.gif, etc.
gif = True          #T/F to generate gif, False to just generate a png
#END customizable values

#change appearance of the maze
baseColor = [0, 255, 0]             #color of the walls
tunnelColor = [255,0,0]             #color of the traversable path
traceColor = [0, 0, 255]            #color of the freshly made traversable path cells
entranceColor = [255, 255, 255]     #color of the entrances/exits of the maze
headColor = [255, 51, 153]          #color of the newest traversable path cells

backtrack_fade_mult = 30            #How quickly the backtrack color fades
head_fade_mult = 3                  #How quickly the head color fades
#END change appearance of the maze

exit_val = -11000
frames=[]   #only used if gif is True
scale = 4

#idk
head_fade_mult *= -3
backtrack_fade_mult *= 3

#returns next available file name with the provided "name_prefix" 
def getFileName(name=name_prefix):
    index = 0
    filename = f'{name}{str(index)}.gif'
    fileExists = os.path.isfile(dir_path + filename)
    while fileExists:
        index = index + 1
        filename = f'{name}{str(index)}.gif'
        fileExists = os.path.isfile(dir_path + filename)
    return filename

#class that defines a maze cell. Consists of 4 walls, a boolean "visited" 
#variable, and a int "value" which is used to color the cell (and maybe do other things)
class Cell:
    def __init__(self):
        self.left = True 
        self.up = True
        self.right = True 
        self.down = True
        self.visited = False
        self.val = 0

#checks if point is within the maze. returns true if it is, false if it is not
def inRange(min, max, x):
    if x < min or x > max:
        return False
    return True

#checks if the indexed cell is a dead end. returns true if it is, false if it is not
def isDeadEnd(i, j, arr):
    count = 0
    if i+1 >= h-1 or arr[i+1][j].visited:
        count += 1
    if i-1 <= 0 or arr[i-1][j].visited:
        count += 1
    if j+1 >= w-1 or arr[i][j+1].visited:
        count += 1
    if j-1 <= 0 or arr[i][j-1].visited:
        count += 1
    if count > 3:
        return True
    return False

#visit a valid neighboring cell
def visitNeighbor(visitStack, dirStack, i, j, arr):
    while(True):
        rand = random.randint(0, 3)
        dirStack.append(rand)
        if rand == 0 and j > 1 and not arr[i][j-1].visited and goodDir(dirStack):
            arr[i][j].left = False
            dirStack.append(0)
            j -= 1
            arr[i][j].right = False
            break
        if rand == 1 and i > 1 and not arr[i-1][j].visited and goodDir(dirStack):
            arr[i][j].up = False
            dirStack.append(1)
            i -= 1
            arr[i][j].down = False
            break
        if rand == 2 and j < w-2 and not arr[i][j+1].visited and goodDir(dirStack):
            arr[i][j].right = False
            dirStack.append(2)
            j += 1
            arr[i][j].left = False
            break
        if rand == 3 and i < h-2 and not arr[i+1][j].visited and goodDir(dirStack):
            arr[i][j].down = False
            dirStack.append(3)
            i += 1
            arr[i][j].up = False
            break
    visitStack.append((i, j))
    arr[i][j].val = head_fade_mult
    arr[i][j].visited = True
    #print(f"(i,j): {i},{j}")
    return i, j

#checks the direction stack to make sure the path is not a simple loop, returns true if it is not - indicating the path is good
def goodDir(dirStack):
    if len(dirStack) < 4:
        return True
    else:
        if dirStack[-4] == [0, 1, 2, 3]:
            return False
        if dirStack[-4] == [1, 2, 3, 0]:
            return False
        if dirStack[-4] == [2, 3, 0, 1]:
            return False
        if dirStack[-4] == [3, 0, 1, 2]:
            return False
    return True

#indicate current cell is being backtraced - for coloring, then backtrack one cell and return its coordinates
def backTrack(visitStack, i, j, arr):
    while(isDeadEnd(i, j, arr)):
        if len(visitStack) <= 0:
            return -1, -1
        arr[i][j].val = backtrack_fade_mult
        if gif:
            appendToGif(arr)
        i, j = visitStack.pop()
    arr[i][j].val = head_fade_mult
    return i, j

#checks if a cell has all of it's walls up - used for appearance. 
def wallsUP(cell):
    if not cell.up:
        return False
    if not cell.right:
        return False
    if not cell.down:
        return False
    if not cell.left:
        return False 

#returns the color of the cell
def getColor(cell, wall):
    if wall:
        return baseColor
    else:
        return calcFadeColor(cell)

#determines the color of the cell based on the cell's value and the customized parameters
def calcFadeColor(cell):
    if not gif or cell.val == 0:
        base = tunnelColor
    if cell.val > 0:
        #colFloor = cell.val - cell.val%9 
        base = []
        for i in range(3):
            mult = cell.val/backtrack_fade_mult
            col_diff = traceColor[i] - tunnelColor[i]
            col_int8 = tunnelColor[i] + mult*col_diff
            base.append(int(col_int8))
        cell.val -= 1
    if cell.val < 0: #Head
        if cell.val < -10000:
            base = entranceColor
            cell.val -= 1
        else:
            base = headColor 
            cell.val += 1  

    return base

#appends the pixel data to the raw gif array
def appendPixel(color, bytes_arr):
    for val in color:
        bytes_arr.append(val)

#Converts cell data to pixel data. Results stored in bytes_arr
def convertToBytes(bytes_arr, cell_arr, bar=None):
    base = [255, 255, 255]; black = baseColor
    for row in cell_arr:
        if bar:
            bar.update()
        for cell in row:
            #top row
            appendPixel(baseColor, bytes_arr)
            col = getColor(cell, cell.up)
            appendPixel(col, bytes_arr)
            appendPixel(baseColor, bytes_arr)
        for cell in row:
            #middle row
            col = getColor(cell, cell.left)
            appendPixel(col, bytes_arr)
            col = getColor(cell, wallsUP(cell))
            appendPixel(col, bytes_arr)
            col = getColor(cell, cell.right)
            appendPixel(col, bytes_arr)
        for cell in row:
            #bottom row 
            appendPixel(baseColor, bytes_arr)
            col = getColor(cell, cell.down)
            appendPixel(col, bytes_arr)
            appendPixel(baseColor, bytes_arr)

#TODO
#Change the scale of the generated gif
def upScale(bytes_arr, scale):
    bytes_arr = bytearray(bytes_arr)
    i = 0   
    max = len(bytes_arr)
    while i < max:
        r = bytes_arr[i]
        g = bytes_arr[i+1]
        b = bytes_arr[i+2]
        for s in range(scale-1):
            bytes_arr.insert(i+3, r)
            bytes_arr.insert(i+4, g)
            bytes_arr.insert(i+5, b)
        i+=3
    return bytes_arr
    # for i in range(len(bytes_arr)):
    #     for s in range(scale+1):
    #         bytes_arr.insert(i+3, bytes_arr[i])
    #         bytes_arr.insert(i+4, bytes_arr[i])
    #         bytes_arr.insert(i+5, bytes_arr[i])

    #     i += 1
        
    #return bytes_arr
#END TODO

#converts a segment of the bytes array to a gif frame and appends it to the gif
def appendToGif(cell_arr):
    bytes_arr = bytearray()
    convertToBytes(bytes_arr, cell_arr)
    #upScale(bytes_arr, scale)
    frames.append(Image.frombytes("RGB", ((w*3), (h*3)), bytes(bytes_arr)))

#Displays information about the programs memory requirements and cell count
def printMem():
    #print(f'size of cell: {sys.getsizeof(Cell())} B')
    byteCount = sys.getsizeof(Cell()) * (w*h) + (w*h * 9 * 3)
    if gif:
        byteCount = sys.getsizeof(Cell()) * (w*h) + (w*h * 9 * 3)*(w*h)
    mb = byteCount / 1000000
    if mb > 999:
        print(f'requires at least {mb/1000} GB')
    else:
        print(f'requires at least {mb} MB')

    if w*h < 1000000:
        print(f'initializing maze with {w*h} cells....')
    else:
        print(f'initializing maze with {round((w*h)/1000000)} million cells....')

#generates an exit on the provided side of the maze
#sides: "left", "right", "up", "down"
#results stored in the cell array "arr"
def createExit(arr, side):
    if side == "left":
        i = random.randint(1, h-2)
        j = 0
        arr[i][j].left = False
        arr[i][j].right = False
        arr[i][j+1].left = False
        arr[i][j].val = exit_val
        arr[i][j+1].val = exit_val
    if side == "right":
        i = random.randint(1, h-2)
        j = w-1
        arr[i][j].left = False
        arr[i][j].right = False
        arr[i][j-1].right = False
        arr[i][j].val = exit_val
        arr[i][j-1].val = exit_val
    if side == "up":
        i = 0
        j = random.randint(1, w-2)
        arr[i][j].up = False
        arr[i][j].down = False
        arr[i+1][j].up = False
        arr[i][j].val = exit_val
        arr[i+1][j].val = exit_val
    if side == "down":
        i = h-1
        j = random.randint(1, w-2)
        arr[i][j].up = False
        arr[i][j].down = False
        arr[i-1][j].down = False
        arr[i][j].val = exit_val
        arr[i-1][j].val = exit_val

#progress bar tracker 
def trackProgress(count, percent):
    percent = round((count/(w*h))*100, 0)
    #print(f'{percent}%')
    #bar.next(percent)
    return percent
