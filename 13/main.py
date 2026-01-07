"""
Script to solve an advent of code problem.
"""

# Standard library imports
import os
import logging
import re
import sys


def main():
   script_directory = os.path.dirname(os.path.abspath(__file__))

   _solve_problem(f"{script_directory}/data_small.txt")
   # Uncomment following line when the problem can be solved with the small data.
   # _solve_problem(f"{script_directory}/data.txt")


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

   with open(data_file, 'r') as file:
      # Read data and solve the problem here instead of passing
      alpha = None
      beta  = None
      a     = None
      b     = None
      c     = None
      d     = None
      e     = None
      f     = None
      num_tokens = 0
      espilon = 0.001
      big_num = 10000000000000
      for line in file:
         if "Button A" in line:
            match = re.search(r"X\+(\d+),\s*Y\+(\d+)", line)
            a, c = map(int, match.groups())

         if "Button B" in line:
            match = re.search(r"X\+(\d+),\s*Y\+(\d+)", line)
            b, d = map(int, match.groups())

         if "Prize" in line:
            match = re.search(r"X=(\d+),\s*Y=(\d+)", line)
            e, f = map(int, match.groups())
            e += big_num
            f += big_num
            beta = (f-(c*e/a)) / ((-c*b/a)+d)
            alpha = (e-(b*beta)) / a

            print()
            print(f"alpha: {alpha}")
            print(f"beta: {beta}")
            
            if abs(alpha - round(alpha)) < espilon and \
               abs(beta - round(beta))   < espilon:
               print("POSSIBLE")
               num_tokens += (3*round(alpha) + round(beta))
            
            print()

      print()
      print(int(num_tokens))
      print()

if __name__ == "__main__":
   main()