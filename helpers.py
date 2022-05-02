from typing import List
from PIL import Image
import random
from array import *
from helpers import *
import sys
import os

w, h = 10, 10
fade_traceback = 99
fade_head = -9
fade_exit = -11000
frames=[]
scale = 4
dir_path = "/home/mot/Documents/GitHub/pyMaze/gifs/"
name_prefix = "maze"

#returns next available file name
def getFileName(name=name_prefix):
    index = 0
    filename = f'{name}{str(index)}.gif'
    fileExists = os.path.isfile(dir_path + filename)
    while fileExists:
        index = index + 1
        filename = f'{name}{str(index)}.gif'
        fileExists = os.path.isfile(dir_path + filename)
    return filename

class Cell:
    def __init__(self):
        self.left = True 
        self.up = True
        self.right = True 
        self.down = True
        self.visited = False
        self.val = 0

def inRange(min, max, x):
    if x < min or x > max:
        return False
    return True


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
    arr[i][j].val = fade_head
    arr[i][j].visited = True
    #print(f"(i,j): {i},{j}")
    return i, j


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


def backTrack(visitStack, i, j, arr):
    while(isDeadEnd(i, j, arr)):
        if len(visitStack) <= 0:
            return -1, -1
        arr[i][j].val = fade_traceback
        bytes_arr = bytearray()
        convertToBytes(bytes_arr, arr)
        #upScale(bytes_arr, scale)
        frames.append(Image.frombytes("RGB", ((w*3), (h*3)), bytes(bytes_arr)))
        i, j = visitStack.pop()
    arr[i][j].val = fade_head
    return i, j


def wallsUP(cell):
    if not cell.up:
        return False
    if not cell.right:
        return False
    if not cell.down:
        return False
    if not cell.left:
        return False 

def getBaseColor(cell):
    if cell.val == 0:
        base = [255, 255, 255]
    if cell.val > 0:
        colRange = int(cell.val/3) * 3
        colVal = 255-int(colRange*(255/(fade_traceback)))
        base = [255, colVal, colVal]
        cell.val -= 1
    if cell.val < 0: #Head
        if cell.val < -10000:
            base = [51, 255, 255]
            cell.val -= 1
        else:
            base = [255, 51, 153]  
            cell.val += 1  

    return base

def convertToBytes(bytes_arr, cell_arr, bar=None):
    base = [255, 255, 255]; black = [0, 0, 0]
    for row in cell_arr:
        if bar:
            bar.update()
        for cell in row:
            base = getBaseColor(cell)
            #top wall
            col = base
            if cell.up or cell.left:
                col = black
            for val in col:
                bytes_arr.append(val)

            col = base
            if cell.up:
                col = black
            for val in col:
                bytes_arr.append(val)

            col = base
            if cell.up or cell.right:
                col = black
            for val in col:
                bytes_arr.append(val)

        for cell in row:
            base = getBaseColor(cell)
            #left wall
            col = base
            if cell.left:
                col = black
            for val in col:
                bytes_arr.append(val)

            #center pixel
            col = base
            if wallsUP(cell):
                col = black
            for val in col:
                bytes_arr.append(val)

            #right wall
            col = base
            if cell.right:
                col = black
            for val in col:
                bytes_arr.append(val)

        for cell in row:
            base = getBaseColor(cell)
            #bottom wall 
            col = base
            if cell.down or cell.left:
                col = black
            for val in col:
                bytes_arr.append(val)

            col = base
            if cell.down:
                col = black
            for val in col:
                bytes_arr.append(val)

            col = base
            if cell.down or cell.right:
                col = black
            for val in col:
                bytes_arr.append(val)

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

def printMem():
    #print(f'size of cell: {sys.getsizeof(Cell())} B')
    byteCount = sys.getsizeof(Cell()) * (w*h) + (w*h * 9 * 3)
    mb = byteCount / 1000000
    if mb > 999:
        print(f'requires at least {mb/1000} GB')
    else:
        print(f'requires at least {mb} MB')

    if w*h < 1000000:
        print(f'initializing maze with {w*h} cells....')
    else:
        print(f'initializing maze with {round((w*h)/1000000)} million cells....')

def createExit(arr, side):
    if side == "left":
        i = random.randint(1, h-2)
        j = 0
        arr[i][j].left = False
        arr[i][j].right = False
        arr[i][j+1].left = False
        arr[i][j].val = fade_exit
        arr[i][j+1].val = fade_exit
    if side == "right":
        i = random.randint(1, h-2)
        j = w-1
        arr[i][j].left = False
        arr[i][j].right = False
        arr[i][j-1].right = False
        arr[i][j].val = fade_exit
        arr[i][j-1].val = fade_exit
    if side == "up":
        i = 0
        j = random.randint(1, w-2)
        arr[i][j].up = False
        arr[i][j].down = False
        arr[i+1][j].up = False
        arr[i][j].val = fade_exit
        arr[i+1][j].val = fade_exit
    if side == "down":
        i = h-1
        j = random.randint(1, w-2)
        arr[i][j].up = False
        arr[i][j].down = False
        arr[i-1][j].down = False
        arr[i][j].val = fade_exit
        arr[i-1][j].val = fade_exit

def trackProgress(count, percent):
    percent = round((count/(w*h))*100, 0)
    #print(f'{percent}%')
    #bar.next(percent)
    return percent
