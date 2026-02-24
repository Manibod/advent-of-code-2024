"""
Script to solve an advent of code problem.
"""

# Standard library imports
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

   SIZE = 70
   POS_START = (0, 0)
   POS_END = (SIZE, SIZE)

   class PosPath:
      def __init__(self, x, y, g):
         self.x = x
         self.y = y
         self.g = g
         self.h = abs(SIZE - x) + abs(SIZE - y)

      def __lt__(self, other):
         return (self.g + self.h) < (other.g + other.h)
   
   class BestCost:
      def __init__(self, g, x_p, y_p):
         self.g   = g
         self.x_p = x_p
         self.y_p = y_p

   byte_coord_list = []
   with open(data_file, 'r') as f:
      for line in f:
         line_split = line.split(',')
         byte_coord_list.append((int(line_split[1]), int(line_split[0])))

   def find_path(num_byte_fallen):
      byte_coord_set = set(byte_coord_list[:num_byte_fallen])
      pos_start = PosPath(0, 0, 0)
      
      grid_pos_best_cost = {}
      grid_pos_best_cost[pos_start] = BestCost(0, 0, 0)

      heap =[]
      heapq.heappush(heap, pos_start)

      while heap:
         pos = heapq.heappop(heap)
         pos_neigh = [PosPath(pos.x - 1, pos.y,     pos.g + 1),
                      PosPath(pos.x + 1, pos.y,     pos.g + 1),
                      PosPath(pos.x,     pos.y - 1, pos.g + 1),
                      PosPath(pos.x,     pos.y + 1, pos.g + 1)]
         for pos_n in pos_neigh:
            if not (0 <= pos_n.x and pos_n.x <= SIZE and 0 <= pos_n.y and pos_n.y <= SIZE) or \
               (pos_n.x, pos_n.y) in byte_coord_set:
               continue

            if ((pos_n.x, pos_n.y) not in grid_pos_best_cost or
               pos_n.g < grid_pos_best_cost[(pos_n.x, pos_n.y)].g):

               grid_pos_best_cost[(pos_n.x, pos_n.y)] = BestCost(pos_n.g, pos.x, pos.y)
               heapq.heappush(heap, PosPath(pos_n.x, pos_n.y, pos_n.g))

               if (pos_n.x, pos_n.y) == POS_END:
                  #-----Printing solution------
                  pos_best_path = set()
                  curr_pos = POS_END
                  while curr_pos != POS_START:
                     pos_best_path.add(curr_pos)
                     curr_pos = (grid_pos_best_cost[curr_pos].x_p, grid_pos_best_cost[curr_pos].y_p)

                  grid_solution = ['.' * (SIZE + 1)] * (SIZE + 1)

                  for bc in byte_coord_set:
                     grid_solution[bc[0]] = grid_solution[bc[0]][:bc[1]] + '#' + grid_solution[bc[0]][bc[1] + 1:]

                  for p in pos_best_path:
                     grid_solution[p[0]] = grid_solution[p[0]][:p[1]] + 'O' + grid_solution[p[0]][p[1] + 1:]
                  
                  # print(f'STEP: {len(pos_best_path)}')

                  with open('./18/grid_solution.txt', 'w') as f:
                     for row in grid_solution:
                        f.write(row + '\n')
                  #-----Printing solution end------

                  return True

      return False
   
   min = 1
   max = len(byte_coord_list)
   last_idx_no_path = max

   while min <= max:
      mid = (max + min) // 2
      # print(f'({byte_coord_list[mid - 1][1]}, {byte_coord_list[mid - 1][0]})')
      if find_path(mid):
         min = mid + 1
      else:
         last_idx_no_path = mid
         max = mid - 1
   
   print(f'({byte_coord_list[last_idx_no_path - 1][1]}, {byte_coord_list[last_idx_no_path - 1][0]})')

# O O O O O O X X X X
# 0 1 2 3 4 5 6 7 8 9
#           5 6 7 8 9
#           5 6
#             6

# O O O X X X X X X X X  X  X  X  X
# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
# 0 1 2 3 4 5 6 
# 0 1 2 
#     2

if __name__ == "__main__":
   main()