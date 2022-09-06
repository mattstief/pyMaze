from typing import List
import PIL
import random
from array import *
from helpers import *
import sys
from tqdm import tqdm

def main():
    visitStack, dirStack = [], []

    printMem()
    #initialize arr 
    cell_arr = [[Cell() for col in range(w)] for row in range(h)]

    i = random.randint(1, h-2)
    j = random.randint(1, w-2)
    visitStack.append((i,j))

    bar = tqdm(total = 100, desc="mapping");       bar.update()
    margin = (w*h)/100;                            tempCount = 0

    while(True):
        #visit unvisited nodes until a dead end is reached
        while(not isDeadEnd(i, j, cell_arr)):
            i,j = visitNeighbor(visitStack, dirStack, i, j, cell_arr)
            
            if gif:
                appendToGif(cell_arr)
            
            tempCount += 1
            if tempCount > margin:
                bar.update()
                tempCount = 0
        #backtrace if at a dead end until a cell with unvisited neighbors is found
        i, j = backTrack(visitStack, i, j, cell_arr)
        #end condition - when all cells are visited
        if i <0 and j < 0:
            break
    
    #end cell generation - close loading bar
    bar.close()
    print("mapping complete. creating image....")

    #convert the cell_arr to raw pixel data for the resulting image
    if gif:
        appendToGif(cell_arr)

    #final image doesn't have any color modifiers (besides for exits done below), so set all the vals to 0
    for row in cell_arr:
        for cell in row:
            cell.val = 0

    if gif:
        appendToGif(cell_arr)

    #generate exits
    createExit(cell_arr, "up")
    createExit(cell_arr, "down")
    createExit(cell_arr, "left")
    createExit(cell_arr, "right")

    #initialize empty byte array
    bytes_arr = bytearray()
    #convert cell_arr to raw pixel data then store in bytes_arr
    convertToBytes(bytes_arr, cell_arr)
    #upScale(bytes_arr, scale) TODO: implement this
    #create image from raw pixel data
    img = Image.frombytes("RGB", ((w*3), (h*3)), bytes(bytes_arr))    

    if gif:
        for a in range(300):
            frames.append(img)
        frame_one = frames[0]
        gifname = getFileName(f'{w}x{h}_Maze')
        frame_one.save(dir_path + gifname, format="GIF", append_images=frames,
                    save_all=True, duration=40, loop=1)
    img.show()  #display the final image in a window
    print("done")

#run main then exit
if __name__ == "__main__":
    sys.exit(main()) 