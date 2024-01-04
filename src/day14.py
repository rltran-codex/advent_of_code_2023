from functools import lru_cache

INPUT_FILE = './resources/day14_input.txt'
# INPUT_FILE = './resources/sample_input/day14.txt'
CYCLE_NUM = 1000000000

cycle_mem = {}

def transpose_pattern(pattern: list):
    """
    Turns the platform so that North is on the left side
    """
    return list(map("".join, zip(*[list(r) for r in pattern])))

def rotate(pattern:list):
    t_mat = list(map(list, zip(*pattern)))
    return list(map(lambda r: ''.join(list(reversed(r))), t_mat))

def calculate_load(platform: list):
    return sum(row.count('O') * (len(platform) - curr_line) for curr_line, row in enumerate([list(r) for r in platform]))

def tilt_north(platform:list):
    n_tilted = []
    for r in platform:
        n_line = []
        for n in r.split("#"):
            l = ['O'] * n.count('O') + ['.'] * n.count('.')
            n_line.append(''.join(l))
        n_tilted.append('#'.join(n_line))
    return n_tilted

def tilt_direction(platform:list):
    n_tilted = []
    for r in platform:
        n_line = []
        for n in r.split("#"):
            l = ['.'] * n.count('.') + ['O'] * n.count('O')
            n_line.append(''.join(l))
        n_tilted.append('#'.join(n_line))
    return n_tilted


# Open file
with open(INPUT_FILE, 'r') as file:
    data = file.read().splitlines()

def part1(data):
    pattern = transpose_pattern(tilt_north(transpose_pattern(data)))
    return calculate_load(pattern)

class AutoCycle:
    def __init__(self, pattern):
        self.pattern = pattern
        self.loop_count = 0
        self.memory = {}

    def cycle(self, pattern : list):
        for i in range(4):
            pattern = rotate(pattern) # rotate so that the next direction
            pattern = tilt_direction(pattern)   # use tilt
        return pattern
    
    def determine_load(self, num):
        """
        Recusive method that checks if detects a loop recuring
        and checks if the memory has had that pattern before.
        """
        # base case
        if (num == 0):
            return calculate_load(self.patttern)
        if (self.loop_count == 50):
            return calculate_load(self.pattern)
        # check if platform config has been in a previous cycle
        key = ''.join(self.pattern)
        
        if key not in self.memory.keys():
            self.memory[key] = self.cycle(self.pattern)
            self.loop_count = 0
        # if so, skip the expensive cycle
        # set current platform to next config platform
        self.pattern = self.memory[key]
        self.loop_count += 1
        return self.determine_load(num - 1) # recur

# Part 1 solution
print(f'Part 1: {part1(data)}')
n = AutoCycle(data)
print(f'Part 1: {n.determine_load(CYCLE_NUM)}')