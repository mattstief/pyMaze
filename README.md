# pyMaze

Dec 2022: I realized that I have encoded the GIF data incorrectly, with 3 Bytes per pixel rather than one. No idea how it works still. 

maze generator with optional gif creation

stuff to tweak is at the top of the helper file

------------
**GIF**

- The pink represents the head. It visits unvisited cells until it reaches a dead end.

- The shades of red represent a backtrack. This happens when a dead end is reached. The head will backtrack until it reaches a cell with unvisited neighbors. Once all cells are visited, the head will backtrack to the beginning cell, indicating completion.

- The end of the gif shows a completed maze with the exits marked with light blue. 

- Blocky and jagged hall style choices

  ![60x60_Maze0](https://user-images.githubusercontent.com/79825665/166346534-e0e2d6a6-0d3d-4696-9be0-739b49488a57.gif) ![60x60_Maze0](https://user-images.githubusercontent.com/79825665/166325381-e8b92078-91a3-4949-8a57-24117b090a43.gif) ![45x45_Maze0](https://user-images.githubusercontent.com/79825665/166355145-b5e793ce-562f-4a93-a4ed-f3300891e153.gif) ![45x45_Maze1](https://user-images.githubusercontent.com/79825665/166369209-a6ca31ab-6e17-49aa-9c43-559084433fbd.gif) ![30x30_Maze0](https://user-images.githubusercontent.com/79825665/166345792-b585adf8-a09d-430f-89a4-0fce7da597d8.gif) ![30x30_Maze0](https://user-images.githubusercontent.com/79825665/166323518-bdaac0f4-b4b4-4902-b383-762ec9e5da20.gif) ![20x20_Maze0](https://user-images.githubusercontent.com/79825665/166345747-45d08846-6ed4-4dc8-bf99-bc2ba4c78545.gif) ![20x20_Maze0](https://user-images.githubusercontent.com/79825665/166340000-4bb7606c-2247-4c56-b8cd-a53cf8c1dd45.gif)



------------

The maze size is greatly limited if creating a gif. I can do 80x80 on my PC. 

If gif creation is off, the maze can be much larger. I got up to 4000x4000 on my PC. 

The bottleneck in both cases is primarily the amount RAM. Thrashing slows the program to a crawl. However, gif creation for "smaller" mazes (<100) is mainly CPU bound.

1000x1000
![1000x1000_Maze](https://user-images.githubusercontent.com/79825665/166328427-1381bc35-3e32-4a0d-89b2-457e517e6c11.PNG)

1800x1800
![1800x1800_Maze](https://user-images.githubusercontent.com/79825665/166332764-c77a7770-e5c9-4e13-81ed-e329a0617803.PNG)
