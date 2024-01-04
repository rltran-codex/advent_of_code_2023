from functools import reduce

# INPUT_FILE = './resources/day15_input.txt'
INPUT_FILE = './resources/sample_input/day15.txt'

with open(INPUT_FILE, 'r') as file:
  data = file.read().split(',')


def hash_str(line : str):
  return reduce(lambda current_val, c: (current_val + ord(c)) * 17 % 256, line, 0)

hash_sum = 0
for d in data:
  hash_sum += hash_str(d)
  print(hash_str(d))
print(hash_sum)