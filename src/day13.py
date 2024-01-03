"""
Day 14: Parabolic Reflector Dish
Reference: https://adventofcode.com/2023/day/14

Post Notes:
For each part, the thought process can be found in each
of the methods, check_mirror_part1 and check_mirror_part2.

Author: Richard Tran
Status: Completed
"""
INPUT_FILE = './resources/day13_input.txt'


def open_file():
    with open(INPUT_FILE, 'r') as file:
        data = {}
        chunk_num = 0
        patterns = [section for section in file.read().split('\n\n')]

        for d in patterns:
            data[chunk_num] = {
                'pattern': d.split('\n'),
                'sum': 0
            }
            chunk_num += 1

        return data


def transpose_pattern(pattern: list):
    """
    Takes the pattern and transposes
    the pattern to process evaluating the columns.
    """
    def to_string(chars: list):
        return ''.join(chars)

    return list(map(to_string, zip(*[list(r) for r in pattern])))


def check_mirror_part1(pattern: list):
    """
    Method first checks if theres a reflection upon the horizontal line, if not,
    then checks for the vertical reflection line.

    Description:
    For Part 1, I solved it by finding a "palindrome" with inspiration
    of the window sliding technique with a modification.
    Letting two arrays, left and right, initially start with the entirety of the rows,
    If the reverse is equal to the ordered, then return the calculated reflection line.
    If not, decrease the windows accordingly (shrink left bound, shrink right bound)
    """
    def findReflectionPoint(eval_pattern: list):
        """
        Inner method that checks if a reflection (palindrome) 
        exists on either the rgt or lft boundary of the pattern

        Returns:
        int: number of rows before the reflection line
        """
        size = len(eval_pattern)
        for idx in range(size):
            lft = eval_pattern[:size - idx]
            rgt = eval_pattern[idx:]

            if lft == lft[::-1] and len(lft) % 2 == 0:
                return int(len(lft) / 2)
            if rgt == rgt[::-1] and len(rgt) % 2 == 0:
                return int((len(rgt) / 2) + idx)

        return None

    reflect = findReflectionPoint(pattern)
    if (reflect):  # horizontal reflection line found
        return 100 * reflect
    else:  # vertical re
        reflect = findReflectionPoint(transpose_pattern(pattern))
        return reflect


def check_mirror_part2(pattern: list):
    """
    Method checks for where the one single smudge is for given pattern
    and returns the summarized number of row/col

    Description:
    To solve part 2, it wasn't trivial since it's just finding a single
    character that differed to the respective reflection.
    However, I wanted it to be a bit more efficient by using the zip() 
    builtin. Thus, I had to break the pattern down into a 2D array,
    then find the number of differences (n).
    """
    def correctSmudge(eval_pattern: list):
        """
        Finds where the smudge is and returns the
        idx of reflection line
        """
        for idx in range(1, len(eval_pattern)):
            lft = eval_pattern[:idx][::-1]
            rgt = eval_pattern[idx:]
            n = sum(sum(0 if a == b else 1 for a, b in zip(x, y))
                    for x, y in zip(lft, rgt))
            if (n == 1):
                return idx
        return 0

    mirror_grid = [list(r) for r in pattern]
    reflect = correctSmudge(mirror_grid)
    if (reflect == 0):
        transpose = [list(r) for r in transpose_pattern(pattern)]
        return correctSmudge(transpose)
    else:
        return reflect * 100


d = open_file()
sum1 = 0
sum2 = 0
for i in d.keys():
    sum1 += check_mirror_part1(d[i]["pattern"])
    sum2 += check_mirror_part2(d[i]["pattern"])
print(sum1)
print(sum2)
