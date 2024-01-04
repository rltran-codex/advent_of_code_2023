
INPUT_FILE = './resources/day15_input.txt'
# INPUT_FILE = './resources/sample_input/day15.txt'

with open(INPUT_FILE, 'r') as file:
  data = file.read().split(',')


def hash_str(line : str):
  line = [c for c in line]
  current_val = 0

  for c in line:
    current_val += ord(c)
    current_val *= 17
    current_val = current_val % 256
  
  return current_val

hash_sum = 0
for d in data:
  hash_sum += hash_str(d)
  print(hash_str(d))
print(hash_sum)