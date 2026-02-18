"""
Script to solve an advent of code problem.
"""

# Standard library imports
from collections import defaultdict

import copy
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
      def __init__(self, x, y, dir, tiles, g):
         self.x   = x
         self.y   = y
         self.dir = dir
         self.tiles = copy.deepcopy(tiles)
         self.tiles.add((self.x, self.y))
         self.g   = g
         self.h   = getHeuristicCost(x, y)
         

      def __lt__(self, other):
         return (self.g + self.h) < (other.g + other.h)

   def getHeuristicCost(x, y):
      return abs(pos_goal[0] - x) + abs(pos_goal[1] - y) + 1000 if abs(pos_goal[0] - x) != 0 and abs(pos_goal[1] - y) != 0 else 0

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
                            E,
                            set(),
                            0)
   maze_pos_best_dir = {}
   maze_pos_best_dir[(pos_path_start.x, pos_path_start.y, E)] = 0
   
   maze_pos_best_cost = {}
   maze_pos_best_cost[(pos_path_start.x, pos_path_start.y)] = 0

   maze_pos_best_parent = defaultdict(list)
   maze_pos_best_parent[(pos_path_start.x, pos_path_start.y)].append(set([(pos_path_start.x, pos_path_start.y)]))

   heap =[]
   heapq.heappush(heap, pos_path_start)

   goal_best_cost = sys.maxsize

   while heap:
      pos_path = heapq.heappop(heap)
      pos_path_tuple = (pos_path.x, pos_path.y)
      pos_path_neigh = [PosPath(pos_path.x-1, pos_path.y,   N, pos_path.tiles, pos_path.g+1+(1000 if N != pos_path.dir else 0)),
                        PosPath(pos_path.x+1, pos_path.y,   S, pos_path.tiles, pos_path.g+1+(1000 if S != pos_path.dir else 0)),
                        PosPath(pos_path.x,   pos_path.y-1, W, pos_path.tiles, pos_path.g+1+(1000 if W != pos_path.dir else 0)),
                        PosPath(pos_path.x,   pos_path.y+1, E, pos_path.tiles, pos_path.g+1+(1000 if E != pos_path.dir else 0))]
      for pos_path_n in pos_path_neigh:
         if ((maze[pos_path_n.x][pos_path_n.y] == "#") or
             (pos_path.dir + pos_path_n.dir) % 2 == 0 and pos_path.dir != pos_path_n.dir or
             ((pos_path_n.g + pos_path_n.h) > goal_best_cost)):
            continue

         pos_n_tuple = (pos_path_n.x, pos_path_n.y)
         pos_n_dir_tuple = (pos_path_n.x, pos_path_n.y, pos_path_n.dir)
         if pos_n_dir_tuple not in maze_pos_best_dir:
            maze_pos_best_dir[pos_n_dir_tuple] = pos_path_n.g
            heapq.heappush(heap, PosPath(pos_path_n.x,
                                         pos_path_n.y,
                                         pos_path_n.dir,
                                         pos_path.tiles, 
                                         pos_path_n.g))

            if pos_n_tuple not in maze_pos_best_cost:
               maze_pos_best_cost[pos_n_tuple] = pos_path_n.g
               maze_pos_best_parent[pos_n_tuple].append(set(list(pos_path.tiles) + [(pos_path_n.x, pos_path_n.y)]))
            elif maze_pos_best_cost[pos_n_tuple] >= pos_path_n.g:
               maze_pos_best_parent[pos_n_tuple].append(set(list(pos_path.tiles) + [(pos_path_n.x, pos_path_n.y)]))

            if pos_n_tuple == pos_goal:
               goal_best_cost = maze_pos_best_cost[pos_n_tuple]

         elif maze_pos_best_cost[pos_n_tuple] >= pos_path_n.g:
               maze_pos_best_parent[pos_n_tuple].append(set(list(pos_path.tiles) + [(pos_path_n.x, pos_path_n.y)]))

   tiles_best_path = set()
   already_path_added = set()
   path_to_add = [pos_goal]

   while path_to_add:
      tile = path_to_add.pop()
      already_path_added.add(tile)
      for path in maze_pos_best_parent[tile]:
         tiles_best_path.update(path)
         for t in path:
            if t not in already_path_added:
               path_to_add.append(t)

   print('-1-')
   print(len(tiles_best_path))
   print('-2-')
   for t in tiles_best_path:
      maze[t[0]] = maze[t[0]][:t[1]] + "O" + maze[t[0]][t[1]+1:]

   for row in maze:
      print(row)

if __name__ == "__main__":
   main()