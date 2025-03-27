"""
Script to solve an advent of code problem.
"""

# Standard library imports
import os
import logging
import sys
import numpy as np

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

   with open(data_file, 'r') as f:
      # Read data and solve the problem here instead of passing
      lines = f.read()
      matrix = np.array([list(l.strip()) for l in lines.splitlines()])
      num_row = matrix.shape[0]
      num_col = matrix.shape[1]
      
      for i in range(4):
         if i != 0:
            matrix = np.rot90(matrix)

         # Lignes
         for i in range(num_row):
            print(''.join(matrix[i]))
         
         # Diag inf
         for i in range(1, num_row):
            print(''.join(matrix.diagonal(-i)))
         
         # Dia main
         print(''.join(matrix.diagonal()))

         # Diag sup
         for i in range(1, num_col):
            print(''.join(matrix.diagonal(i)))
   
   # python main.py | "C:\Program Files\Git\usr\bin\grep.exe" -o "XMAS" | wc -l

if __name__ == "__main__":
   main()
