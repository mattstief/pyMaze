# pyMaze
maze generator with optional gif creation

stuff to tweak is at the top of the helper file

------------
**GIF**

- The pink represents the head. It visits unvisited cells until it reaches a dead end.

- The shades of red represent a backtrack. This happens when a dead end is reached. The head will backtrack until it reaches a cell with unvisited neighbors. Once all cells are visited, the head will backtrack to the beginning cell, indicating completion.

- The end of the gif shows a completed maze with the exits marked with light blue. 

  ![60x60_Maze0](https://user-images.githubusercontent.com/79825665/166325381-e8b92078-91a3-4949-8a57-24117b090a43.gif)
![30x30_Maze0](https://user-images.githubusercontent.com/79825665/166323518-bdaac0f4-b4b4-4902-b383-762ec9e5da20.gif)
![30x30_Maze1](https://user-images.githubusercontent.com/79825665/166323579-52812f5b-5928-4d3c-9e5e-72b5a6e46f16.gif)
![30x30_Maze2](https://user-images.githubusercontent.com/79825665/166323587-25fcb7ac-bbf4-44b6-a79e-371401f48df9.gif)

------------

The maze size is greatly limited if creating a gif. I can do 80x80 on my PC. 

If gif creation is off, the maze can be much larger. I got up to 4000x4000 on my PC. 

The bottleneck in both cases is primarily the amount RAM. Thrashing slows the program to a crawl. However, gif creation for "smaller" mazes (<100) is mainly CPU bound.
![1000x1000_Maze](https://user-images.githubusercontent.com/79825665/166328427-1381bc35-3e32-4a0d-89b2-457e517e6c11.PNG)
