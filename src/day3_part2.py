"""
-- Part II --
The missing part wasn't the only issue - one of the gears in the engine is wrong.
A gear is any * symbol that is adjacent to exactly two part numbers. 

Consider the same engine schematic again:

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

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35,
so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490.

What is the sum of all the gear ratios in the engine schematic (puzzle input)

-- Note --
This implementation contains multiple functions to address the complexity of the problem.
Breaking down the problem into smaller functions helped identify edge cases, such as determining
whether a symbol is truly positioned next to two numbers. The approach involved visualizing a "bubble,"
where, if a number resided in any corner of the bubble, it was
potentially next to two numbers. Refer to the methods for more information:
  - check_upper_bubble
  - check_lower_bubble
  - check_right_bubble
  - check_left_bubble


Reference: https://adventofcode.com/2023/day/3

Author: Richard Tran
Status: Completed
"""
import time
from day3_part1 import is_number, INPUT_FILE
from functools import reduce
import re

engine_schematic = []
schar_indices = []
sum_2 = 0


def validate_gear_number(row, col, schar_loc: tuple) -> bool:
    """
    Method takes two parameters, row and col,
    and checks if the number in the 2D array
    is adjacent/diagonal to target special chars
    """
    eval_positions = [
        (row-1, col),  # above of symbol
        (row+1, col),  # below of symbol
        (row, col-1),  # left of symbol
        (row, col+1),  # right of symbol
        (row-1, col-1),  # diagonal up left
        (row-1, col+1),  # diagonal up right
        (row+1, col-1),  # diagonal dwn left
        (row+1, col+1)  # diagonal dwn right
    ]

    # check if any of the position calculations equal to the location of the gear symbol
    for i, j in eval_positions:
        if i == schar_loc[0] and j == schar_loc[1]:
            return True

    return False


def build_number_on_row(row, schar_loc):
    col = 0
    nums = []
    try:
        while col < len(engine_schematic[row]):
            if (not is_number(engine_schematic[row][col])):
                col += 1
                continue

            num = ''
            is_valid_gear_num = False
            while True:
                if col > len(engine_schematic[row]) - 1:
                    break

                if (not is_number(engine_schematic[row][col])):
                    break

                num += engine_schematic[row][col]
                if (not is_valid_gear_num):
                    is_valid_gear_num = validate_gear_number(
                        row, col, schar_loc=schar_loc)
                col += 1

            if is_valid_gear_num:
                nums.append(int(num))
    except IndexError:
        pass

    return nums


def check_upper_bubble(schar_row: int, schar_col: int) -> bool:
    """
    Method checks if a number is present in the "southern hemisphere" of 
    the symbol position to check.

    Ex:
    [x][x][x]
    [ ][*][x]
    [ ][ ][ ]
    Where x is the location of evaluation points
    """
    eval_positions = [
        (schar_row-1, schar_col),  # above of symbol
        (schar_row,   schar_col+1),  # right of symbol
        (schar_row-1, schar_col-1),  # diagonal up left
        (schar_row-1, schar_col+1),  # diagonal up right
    ]

    for i, j in eval_positions:
        try:
            if (is_number(engine_schematic[i][j])):
                return True
        except IndexError:
            pass


def check_lower_bubble(schar_row: int, schar_col: int) -> bool:
    """
    Method checks if a number is present in the "southern hemisphere" of 
    the symbol position to check.

    Ex:
    [ ][ ][ ]
    [x][*][ ]
    [x][x][x]
    Where x is the location of evaluation points
    """
    eval_positions = [
        (schar_row+1, schar_col),  # below of symbol
        (schar_row,   schar_col-1),  # left of symbol
        (schar_row+1, schar_col-1),  # diagonal dwn left
        (schar_row+1, schar_col+1)  # diagonal dwn right
    ]

    for i, j in eval_positions:
        try:
            if (is_number(engine_schematic[i][j])):
                return True
        except IndexError:
            pass

    return False


def check_right_bubble(schar_row: int, schar_col: int) -> bool:
    """
    Method checks if a number is present in the right side of 
    the row and col to check.

    Ex:
    [ ][x][x]
    [ ][*][x]
    [ ][ ][x]
    Where x is the location of evaluation points
    """
    eval_positions = [
        (schar_row-1, schar_col),  # above of symbol
        (schar_row,   schar_col+1),  # right of symbol
        (schar_row-1, schar_col+1),  # diagonal up right
        (schar_row+1, schar_col+1)  # diagonal dwn right
    ]

    for i, j in eval_positions:
        try:
            if (is_number(engine_schematic[i][j])):
                return True
        except IndexError:
            pass

    return False


def check_left_bubble(schar_row: int, schar_col: int) -> bool:
    """
    Method checks if a number is present in the left side of 
    the row and col to check.

    Ex:
    [x][ ][ ]
    [x][*][ ]
    [x][x][ ]
    Where x is the location of evaluation points
    """
    eval_positions = [
        (schar_row+1, schar_col),  # below of symbol
        (schar_row,   schar_col-1),  # left of symbol
        (schar_row+1, schar_col-1),  # diagonal dwn left
        (schar_row-1, schar_col-1),  # diagonal up left
    ]

    for i, j in eval_positions:
        try:
            if (is_number(engine_schematic[i][j])):
                return True
        except IndexError:
            pass

    return False


def calculate_gear_ratio(gear: tuple) -> int:
    # if the symbol fails the "bubble" check, then return 0
    if (not (check_upper_bubble(row, col) and check_lower_bubble(row, col))
            and not (check_left_bubble(row, col) and check_right_bubble(row, col))):
        return 0

    gear_num = []

    # build int number one row above
    above_row = build_number_on_row(gear[0] - 1, gear)
    # build int number on the same row
    same_row = build_number_on_row(gear[0], gear)
    # build int number one row below
    below_row = build_number_on_row(gear[0] + 1, gear)
    gear_num = above_row + same_row + below_row
    if len(gear_num) != 2:  # gear number is valid if and only if it is next to exactly two nu mbers
        return 0
    return reduce(lambda x, y: x * y if isinstance(x, int)
                  and isinstance(y, int) else x, gear_num)


if __name__ == "__main__":
    with open(INPUT_FILE, 'r') as file:
        # read each line -> list of characters -> add to engine_schematic (2D array)
        lines = [line.strip() for line in file]
        for l in lines:
            pattern = re.compile(r'[^a-zA-Z0-9.]+')
            i = [m.start() for m in list(pattern.finditer(l))]
            engine_schematic.append(list(l))
            schar_indices.append(i)

    # iterate through special char indicies
    # check if row consists of a special char, else goto next row
    # check for symbols that are next to two numbers
        # using a "bubble", check northern and southern part of the bubble,
        # then check left and right
        # if not found, then the symbol is not near two numbers
    start = time.time()
    for row, list in enumerate(schar_indices):
        for col in list:
            sum_2 += calculate_gear_ratio((row, col))
    end = time.time()
    print(f"Part II answer: {sum_2}")
    print(f"Time: {(end - start) * 10**3} ms")

