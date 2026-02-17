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

   #_solve_problem(f"{script_directory}/data_small.txt")
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

   class PosPath:
      def __init__(self, x, y, x_p, y_p, dir, g):
         self.x   = x
         self.y   = y
         self.x_p = x_p
         self.y_p = y_p
         self.dir = dir
         self.g   = g
         self.h   = getHeuristicCost(x, y)

      def __lt__(self, other):
         return (self.g + self.h) < (other.g + other.h)

   class PosBest:
      def __init__(self, x_p, y_p, g, h):
        self.x_p = x_p
        self.y_p = y_p
        self.g   = g
        self.h   = h

   def getHeuristicCost(x, y):
      return abs(pos_goal[0] - x) + abs(pos_goal[1] - y) + 1000 if abs(pos_goal[0] - x) != 0 and abs(pos_goal[1] - y) != 0 else 0

   def getNeigh(pos_path):
      return [PosPath(pos_path.x-1, pos_path.y,   pos_path.x, pos_path.y, N, pos_path.g+1+(1000 if N != pos_path.dir else 0)),
              PosPath(pos_path.x+1, pos_path.y,   pos_path.x, pos_path.y, S, pos_path.g+1+(1000 if S != pos_path.dir else 0)),
              PosPath(pos_path.x,   pos_path.y-1, pos_path.x, pos_path.y, W, pos_path.g+1+(1000 if W != pos_path.dir else 0)),
              PosPath(pos_path.x,   pos_path.y+1, pos_path.x, pos_path.y, E, pos_path.g+1+(1000 if E != pos_path.dir else 0))]

   maze = []
   with open(data_file, 'r') as f:
      for line in f:
         if not line:
            continue
      
         maze.append(line.rstrip())
         # print(line.rstrip())

   pos_start = (len(maze) - 2, 1)
   pos_goal = (1, len(maze[1])-2)
   pos_path_start = PosPath(len(maze) - 2,
                            1,
                            len(maze) - 2,
                            1,
                            E,
                            0)
   maze_pos_best = defaultdict(list)
   maze_pos_best[(pos_path_start.x, pos_path_start.y)].append(PosBest(len(maze) - 2, 1, 0, getHeuristicCost(pos_path_start.x, pos_path_start.y)))

   heap =[]
   heapq.heappush(heap, pos_path_start)

   goal_best_cost = sys.maxsize
   tiles_best_path = set()

   while heap:
      pos_path = heapq.heappop(heap)
      pos_trace = (pos_path.x, pos_path.y)
      pos_trace_2 = None
      pos_path_neigh = getNeigh(pos_path)
      for pos_path_n in pos_path_neigh:
         if ((maze[pos_path_n.x][pos_path_n.y] == "#") or
             (pos_path.dir + pos_path_n.dir) % 2 == 0 and pos_path.dir != pos_path_n.dir or
             ((pos_path_n.g + pos_path_n.h) > goal_best_cost)):
            continue

         pos_n_tuple = (pos_path_n.x, pos_path_n.y)
         if (not maze_pos_best[pos_n_tuple] or
             pos_path_n.g <= maze_pos_best[pos_n_tuple][0].g or
             (pos_path_n.g == maze_pos_best[pos_n_tuple][0].g + 1000)):

            maze_pos_best[pos_n_tuple].append(PosBest(pos_path_n.x_p,
                                                      pos_path_n.y_p,
                                                      pos_path_n.g,
                                                      pos_path_n.h))
            heapq.heappush(heap, PosPath(pos_path_n.x,
                                         pos_path_n.y,
                                         pos_path_n.x_p,
                                         pos_path_n.y_p,
                                         pos_path_n.dir,
                                         pos_path_n.g))

            if pos_n_tuple == pos_goal:
               goal_best_cost = maze_pos_best[pos_n_tuple][0].g

   def get_paths(pos):
      if pos in tiles_best_path:
        return
      tiles_best_path.add(pos)
      if pos == pos_start:
         return
      for pos_best in maze_pos_best[pos]:
         get_paths((pos_best.x_p, pos_best.y_p))

   get_paths(pos_goal)

   print('-1-')
   print(len(tiles_best_path))
   print('-2-')
   for t in tiles_best_path:
      maze[t[0]] = maze[t[0]][:t[1]] + "O" + maze[t[0]][t[1]+1:]

   for row in maze:
      print(row)

if __name__ == "__main__":
   main()