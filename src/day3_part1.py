"""
-- Part I --
The engine schematic (your puzzle input) consists of a visual representation of the engine. 
There are lots of numbers and symbols, but any number adjacent to a symbol, even diagonally, 
is a "part number". (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right).
Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

What is the sum of all of the part numbers in the engine schematic?

Reference: https://adventofcode.com/2023/day/3

Author: Richard Tran
Status: Completed
"""
import re

INPUT_FILE = "./resources/day3_input.txt"
sum_1 = 0

part_numbers = []     # array to hold valid part numbers
engine_schematic = [] # 2D array to load each character per line in INPUT_FILE

def validate_part_number(row, col) -> bool:
  """
  Method takes two parameters, row and col,
  and checks if the character in the 2D array
  is adjacent/diagonal to special chars
  """
  eval_positions = [
                    (row-1, col),  # above of symbol
                    (row+1, col),  # below of symbol
                    (row, col-1),  # left of symbol
                    (row, col+1),  # right of symbol
                    (row-1, col-1), # diagonal up left
                    (row-1, col+1), # diagonal up right
                    (row+1, col-1), # diagonal dwn left
                    (row+1, col+1)  # diagonal dwn right
                ]
  
  for i, j in eval_positions:
    try:
      char = engine_schematic[i][j]
      if (re.search(r'[^a-zA-Z0-9.]+', char)):
        return True
    except IndexError:
      pass
    
  return False

def is_number(char : str):
  return bool(re.search(r'\d', char))

if __name__ == "__main__":
  
  # open file and load engine_schematic : 2D array
  with open(INPUT_FILE, 'r') as file:
    # read each line -> list of characters -> add to engine_schematic (2D array)
    engine_schematic = [list(line.strip()) for line in file]

  
  # iterate through 2D array
  for row, line in enumerate(engine_schematic):
    idx = 0
    while idx < len(line):
      # check if line[idx] is a number
      if (not is_number(line[idx])):
        idx += 1
        continue

      # build number by iterating ahead
      # at the same time check if there are any adjacent/diagonal special chars
      num = ''
      is_valid_part = False
      while True:
        if idx > len(line) - 1:        # break condition 1
          break
        if (not is_number(line[idx])): # break condition 2
          break

        num += line[idx]
        if (not is_valid_part): # if number is still invalid, check if it COULD be valid
          is_valid_part = validate_part_number(row, col=idx)
        idx += 1

      
      # if valid, then add to part numbers
      if is_valid_part:
        part_numbers.append(int(num))
      # skip n columns for next iteration
    
  
  # find the sum of all valid part numbers
  for num in part_numbers:
    sum_1 += num

  print(f"Part I  answer: {sum_1}")