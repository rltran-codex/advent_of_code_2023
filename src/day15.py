"""
Day 15: Lens Library
Part I
The HASH algorithm is a way to turn any string of characters into a single number in the range 0 to 255. 
To run the HASH algorithm on a string, start with a current value of 0. 
Then, for each character in the string starting from the beginning:

    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.

Part II
The book goes on to describe a series of 256 boxes numbered 0 through 255. The boxes are arranged in a line starting from the point where light enters the facility.
The boxes have holes that allow light to pass from one box to the next all the way down the line.
dash (-), go to the relevant box and remove the lens with the given label if it is present in the box.
Then, move any remaining lenses as far forward in the box as they can go without changing their order, filling any space made by removing the indicated lens.
equals sign (=), it will be followed by a number indicating the focal length of the lens that needs to go into the relevant box
be sure to use the label maker to mark the lens with the label given in the beginning of the step so you can find it later.


Post Notes:
This is simply a hashing and collision problem for data structures.
So to make life a little simple, I used two dictionaries. One that stores
the information about the operational characters, the box number, 
the index it can be found at, and the current value. The other contains the list of lenses
stored in the box.

Author: Richard L Tran
Status: Completed
"""
from functools import reduce
import re

INPUT_FILE = './resources/day15_input.txt'
# INPUT_FILE = './resources/sample_input/day15.txt'

boxes = {}
op_char = {}


def init_hash():
  for i in range(256):
    boxes[i] = []

  with open(INPUT_FILE, 'r') as file:
    data = file.read().split(',')
    for d in data:
      result = re.match(r'^(.*?)(?=[-=])', d).group(1)
      # 'info' = [BOX NUMBER, INDEX NUMBER, CURRENT LENSE VAL]
      op_char[result] = [hash_str(result), None, None]

  
  return data


def hash_str(line : str):
  return reduce(lambda current_val, c: (current_val + ord(c)) * 17 % 256, line, 0)

def load_lense(op : str):
  char, lense_val = re.split(r'[-=]', op)
  box_num, idx_loc, len_val = op_char[char]
  box = boxes[box_num]

  if '-' in op:
    if idx_loc != None: # if lense stored then remove
      box.pop(idx_loc)
      idx_loc = None
      len_val = None
      op_char.update({char : [box_num, idx_loc, len_val]})

      # now that an item is removed, it may effect indexings of other items
      for i, l in enumerate(box): # update all indexes
        c, lv = l.split("=")
        op_char.update({c : [box_num, i, int(lv)]})
  else:
    if idx_loc != None: # update lense
      box[idx_loc] = op
      op_char.update({char : [box_num, idx_loc, int(lense_val)]})
    else: # insertion
      box.append(op)
      op_char.update({char : [box_num, len(box) - 1, int(lense_val)]})

  boxes.update({box_num : box})

data = init_hash()
# Part I
hash_sum_part1 = 0
hash_sum_part2 = 0
for d in data:
  hash_sum_part1 += hash_str(d) # Part I
  load_lense(d)                 # Part II
print(hash_sum_part1)

add_lambda = lambda x, t, z: (x + 1) * (t + 1) * z
for x, y in op_char.items():
  if None not in y:
    hash_sum_part2 += add_lambda(*y)
print(hash_sum_part2)