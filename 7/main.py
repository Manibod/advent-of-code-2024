"""
Script to solve an advent of code problem.
"""

# Standard library imports
import os
import logging
import sys
import copy


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

   current_result = 0
   with open(data_file, 'r') as f:
      # Read data and solve the problem here instead of passing
      for line in f:
         if not line:
            continue
      
         line_splitted = line.split(':')
         test_value = int(line_splitted[0])
         numbers = list(map(int, line_splitted[1].split()))
         #print(f'{test_value}: {numbers}')

         assert len(numbers) > 0

         current_result += test_value if is_possible(test_value, "", numbers) else 0

   print(current_result)

def is_possible(current_sum, operator, numbers_list):
   #print(f'{current_sum}   {operator}     {numbers_list}\n')
   if not numbers_list:
      return (operator == "*" and current_sum == 1) or (operator == "+" and current_sum == 0)
   
   numbers_list_copy = copy.deepcopy(numbers_list)
   last_number = numbers_list_copy.pop()
   if last_number > current_sum:
      return False
   
   if current_sum % last_number != 0:
      return is_possible(current_sum - last_number, "+", numbers_list_copy)
   else:
      return is_possible(current_sum - last_number, "+", numbers_list_copy) or is_possible(current_sum / last_number, "*", numbers_list_copy)

if __name__ == "__main__":
   main()