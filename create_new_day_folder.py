""" 
Use this script to create a folder containing files to solve an advent of code problem for a 
specific day.
"""


# Standard library imports
import argparse
import datetime
import logging
import os
import shutil
import sys
import webbrowser


def main():
   parser = argparse.ArgumentParser(description="Script to create a folder corresponding to the day\
                                                 given as a parameter and open the advent of code  \
                                                 problem corresponding to the given day for the    \
                                                 current year in the web browser.                  \
                                                 The created folder will contain a python script   \
                                                 and data files that will be read by the python    \
                                                 script .")
   parser.add_argument('day', type=int, help="Day for which a python script and data must be created.")
   args = parser.parse_args()

   day_folder = f"{os.getcwd()}//{args.day}"
   if os.path.isdir(day_folder):
      logging.error(f"Day {args.day} already exists.")
      sys.exit(1)

   template_file = f"{os.getcwd()}//new_day_template.py"
   if not os.path.isfile(template_file):
      logging.error("Template file (new_day_template.py) is not at the root.")
      sys.exit(1)

   # Create folder and template files
   os.mkdir(day_folder)
   shutil.copyfile(template_file, f"{day_folder}//main.py")
   with open(f"{day_folder}//data_small.txt", 'w'):
      pass

   with open(f"{day_folder}//data.txt", 'w'):
      pass

   # Open Advent of code problem in the browser since the input relies on cookies
   year = datetime.datetime.now().year
   webbrowser.open(f"https://adventofcode.com/{year}/day/{args.day}")


if __name__ == "__main__":
   main()