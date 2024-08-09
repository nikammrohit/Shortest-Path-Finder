import curses
from curses import wrapper
import queue
import time


maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze, stdscr, path=[]):

    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate (maze): #enumerate will give us an index and the value. It will return the row as a row and i will be which row you are on.
        for j, value in enumerate(row): #the column
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE) #tells user whaever position it is on based on its value

def find_start(maze, start): #looks for start position "O" in maze via each row and column
    for i, row in enumerate(maze): 
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start) #sets starting position var from value we got in previous func
    
    q = queue.Queue() #first in first out data structure
    q.put((start_pos, [start_pos])) #adds start position and places it into list to be stored so it is not evaluated later and so the path can be drawn on screen for each node if it reaches the target

    visited = set() #contains all positions we currently visited

    while not q.empty():
        current_pos, path = q.get() #gets most recent elements path and position
        row, col = current_pos

        stdscr.clear()
        print_maze(maze,stdscr, path)#path allows us to draw the path so we can see the progress going on as we print the maze
        time.sleep(0.2) #slows down animation to show algorithm work in action
        stdscr.refresh()

        if maze[row][col] == end: #if position (from most recent element) = X then we found end of maze
            return path #return path since we found end node
        
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors: #loop through valid neighbor positions and if they are valid add them to path and add them to queue so we check if they are the end node and if we need to expand from that
            if neighbor in visited: #if we already visited then continue and skip 
                continue

            r, c = neighbor
            if maze[r][c] == "#": #if neighbor is an obstacle then skip
                continue
            
            new_path = path + [neighbor]
            q.put((neighbor, new_path)) #process neighbor and add it to queue (new_path = current path + current neighbor that we are considering)
            visited.add(neighbor) #add neighbor to the visited set

def find_neighbors(maze, row, col): #look up, left, right, and down to determine if neighbor is a position or an obstacle
    neighbors = []

    if row > 0: #checks up
        neighbors.append((row-1, col)) #ensures we have not hit bounds of maze
    if row + 1 < len(maze): #checks down
        neighbors.append((row+1, col))
    if col > 0: #checks left
        neighbors.append((row, col-1))
    if col+1 < len(maze[0]): #checks right. maze may not be square
        neighbors.append((row, col+1))

    return neighbors


def main(stdscr):

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #foreground background color assigned to a specific ID
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch() #get char/input from user to exit


wrapper(main)