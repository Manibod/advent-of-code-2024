"""
Script to solve an advent of code problem.
"""

# Standard library imports
from collections import defaultdict

import heapq
import os
import logging
import sys

def main():
   script_directory = os.path.dirname(os.path.abspath(__file__))

   # _solve_problem(f"{script_directory}/data_small.txt")
   # Uncomment following line when the problem can be solved with the small data.
   _solve_problem(f"{script_directory}/data.txt")


def _solve_problem(data_file):
   "Function to solve the corresponding advent of code problem using the data in 'data_file'."
   # Ensure that data file exists
   if not os.path.isfile(data_file):
      logging.error("Data file does not exist.")
      sys.exit(1)

   # Ensure that input exists
   if os.path.getsize(data_file) <= 0:
      logging.error("Data file is still empty.")
      sys.exit(1)

   N = 0
   E = 1
   S = 2
   W = 3

   class TilePath:
      def __init__(self, x, y, x_p, y_p, dir, g):
         self.x   = x
         self.y   = y
         self.x_p = x_p
         self.y_p = y_p
         self.dir = dir
         self.g   = g
         self.h   = abs(pos_goal[0] - x) + abs(pos_goal[1] - y)
   
   class BestCost:
      def __init__(self, x_p, y_p, g):
         self.x_p = x_p
         self.y_p = y_p
         self.g   = g

   def getNeigh(tile):
      return [TilePath(tile.x-1, tile.y,   tile.x, tile.y, N, tile.g+1+(1000 if N != tile.dir else 0)),
              TilePath(tile.x+1, tile.y,   tile.x, tile.y, S, tile.g+1+(1000 if S != tile.dir else 0)),
              TilePath(tile.x,   tile.y-1, tile.x, tile.y, W, tile.g+1+(1000 if W != tile.dir else 0)),
              TilePath(tile.x,   tile.y+1, tile.x, tile.y, E, tile.g+1+(1000 if E != tile.dir else 0))]

   maze = []
   with open(data_file, 'r') as f:
      for line in f:
         if not line:
            continue
         maze.append(line.rstrip())

   pos_start = (len(maze) - 2, 1)
   pos_goal = (1, len(maze[1])-2)
   tile_start = TilePath(len(maze) - 2,
                         1,
                         len(maze) - 2,
                         1,
                         E,
                         0)
   maze_pos_best_cost = defaultdict(list)
   maze_pos_best_cost[(tile_start.x, tile_start.y)].append()

   heap =[]
   heapq.heappush(heap, tile_start)

   goal_found = False

   while heap and not goal_found:
      tile = heapq.heappop(heap)
      tile_neigh = getNeigh(tile)
      for tile_n in tile_neigh:
         if ((maze[tile_n.x][tile_n.y] == "#") or
             (tile.dir + tile_n.dir) % 2 == 0 and tile.dir != tile_n.dir):
            continue
         
         pos_n_tuple = (tile_n.x, tile_n.y)
         if (pos_n_tuple not in maze_pos_best_cost or
             tile_n.g < maze_pos_best_cost[pos_n_tuple]):

            maze_pos_best_cost[pos_n_tuple] = tile_n.g
            heapq.heappush(heap, TilePath(tile_n.x, tile_n.y, tile_n.dir, tile_n.g))

            if pos_n_tuple == pos_goal:
               print(maze_pos_best_cost[pos_n_tuple])
               goal_found = True
               break

if __name__ == "__main__":
   main()
