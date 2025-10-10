"""
Script to solve an advent of code problem.
"""

# Standard library imports
import os
import logging
import sys

from minizinc import Instance, Model, Solver
from collections import defaultdict

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
   
   directory = os.path.dirname(data_file)

   generate_minizinc_data(data_file, directory)
   results = call_minizinc_solver(directory)
   post_process_solution(results, True)

def generate_minizinc_data(data_file, directory):
   # Print data formatted for Minizinc
   matrix_data = "matrix = ["
   white_space_padding = len(matrix_data)
   num_row = -1
   num_col = 0
   first_line = True
   with open(data_file, 'r') as f:
      for line in f:
         if not line or line == '\n':
            continue
         line = line.strip()

         row = "|"

         for i in range(len(line)):
            row += f'{line[i]}, '
         row = row[:-2]
         if not first_line:
            matrix_data += white_space_padding * ' '
         matrix_data += f'{row}\n'

         num_row = len(line)
         num_col += 1

         first_line = False

   matrix_data += white_space_padding * ' '
   matrix_data += "|];\n"

   # Write the data in a file
   with open(f"{directory}/minizinc_data.dzn", "w") as f:
      f.write(f'num_row = {num_row};\n')
      f.write(f'num_col = {num_col};\n')
      f.write(matrix_data)
      f.write(f'path_length = 10;\n')

def call_minizinc_solver(directory):
   model = Model(f'{directory}/minizinc_model.mzn')
   model.add_file(f'{directory}/minizinc_data.dzn')
   gecode = Solver.lookup('gecode')
   instance = Instance(gecode, model)
   results = instance.solve(all_solutions=True)
   if results.status.name != 'ALL_SOLUTIONS':
      raise RuntimeError('Unsatisfiable problem')
   return results

def post_process_solution(results, count_distinct_path=False):
   num_paths_dict = defaultdict(int)
   for i in range(len(results)):
      path = results[i, 'path']
      path_key = f'{path[0]['row']},{path[0]['column']}-{path[9]['row']},{path[9]['column']}'
      num_paths_dict[path_key] += 1

   print(len(num_paths_dict.keys())) if count_distinct_path else print(sum(num_paths_dict.values()))

if __name__ == "__main__":
   main()