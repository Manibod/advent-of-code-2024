"""
Script to solve an advent of code problem.
"""

# Standard library imports
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

   with open(data_file, 'r') as f:
      # Read data and solve the problem here instead of passing
      # list1 = []
      # list2 = []

      # for line in f:
      #    if not line:
      #       continue

      #    line_split = line.split()
      #    number_list1 = int(line_split[0])
      #    number_list2 = int(line_split[1])
      #    # print(f'{number_list1} {number_list2}')

      #    list1.append(number_list1)
      #    list2.append(number_list2)

      # list1.sort()
      # list2.sort()

      # total_dist = 0
      # for i in range(len(list1)):
      #    total_dist += abs(list1[i] - list2[i])

      # print()
      # print(total_dist)

      left_dict = {}
      right_list = []
      for line in f:
         line_split = line.split()
         number_right = int(line_split[0])
         number_left = int(line_split[1])
         if number_left in left_dict:
            left_dict[number_left] += 1
         else:
            left_dict[number_left] = 0
      
         
         

if __name__ == "__main__":
   main()