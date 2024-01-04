INPUT_FILE = './resources/day14_input.txt'

def transpose_pattern(pattern: list):
    """
    Turns the platform so that North is on the left side
    """
    return list(map("".join, zip(*[list(r) for r in pattern])))

def calculate_load(platform: list):
    return sum(row.count('O') * (len(platform) - curr_line) for curr_line, row in enumerate([list(r) for r in platform]))

def tilt_north(platform:list):
    platform = transpose_pattern(platform)
    n_tilted = []
    for r in platform:
        n_line = []
        for n in r.split("#"):
            l = ['O'] * n.count('O') + ['.'] * n.count('.')
            n_line.append(''.join(l))
        n_tilted.append('#'.join(n_line))
    return transpose_pattern(n_tilted)


# Open file
with open(INPUT_FILE, 'r') as file:
    data = file.read().splitlines()

# Part 1 solution
print(f'Part 1: {calculate_load(tilt_north(data))}')