"""
For each row, the condition records show every spring and whether it is operational (.) or damaged (#). 
This is the part of the condition records that is itself damaged; for some springs, 
it is simply unknown (?) whether the spring is operational or damaged.

In the puzzle input, there contains a a given row, the size of each contiguous group of damaged 
springs is listed in the order those groups appear in the row. This list always accounts 
for every damaged spring, and each number is the entire size of its contiguous group
Your job is to figure out how many different arrangements of operational and broken springs fit 
the given criteria in each row.


Notes:
A permutation is a (possible) rearrangement of objects. 
A row is valid if each group is separated by '.' and be in the same order as the combo
 - #.#.### with 1,1,3 combo is valid, but ##..### with 1,1,3 combo is not valid.
 - ####.##.## with 2,2,4 is valid in the sense of separation, but not valid due to order of combo.

References:
https://www.baeldung.com/cs/array-generate-all-permutations
"""
import re

INPUT_FILE = './resources/day12_input.txt'

def validate(line : str, numbers : list):
  """
  Validates the spring row if it matches with the group number combo

  Parameters:
  - line: spring row
  - numbers: group combo
  """
  return [len(spring) for spring in re.findall(r'#+', line)] == numbers



# first load an initial valid string of the combination
# recursively swap things to find the number of possible combinations
# need a way to track which arrays are valid to move around
# for each ?, it can be either . or #


def open_file():
  with open(INPUT_FILE, 'r') as file:
    lines = file.readlines()
    data = {}
    for idx, line in enumerate(lines):
      unk_springs = line.split(" ")[0]
      num_combo = [int(num) for num in re.findall(r'\d+', line.split(" ")[1])]

      data[idx] = {
        'springs' : unk_springs,
        'numbers' : num_combo
      }

    return data


if __name__ == '__main__':
  springs = open_file()

  for s_data in springs.values():
    line = s_data['springs']
    nums = s_data['numbers']
    replaceable = [False if char != '?' else True for char in line]
    print(replaceable)
