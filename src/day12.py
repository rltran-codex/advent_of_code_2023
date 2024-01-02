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

Post Notes:
I got stuck on this problem initially as I was trying to create an efficient recursive 
solution. As a result, I will note this problem as something for myself to improve on
in terms of dynamic programming and memoization

References:
https://github.com/maneatingape/advent-of-code-rust/blob/main/src/year2023/day12.rs
https://github.com/Domyy95/Challenges/blob/master/2023-12-Advent-of-code/12.py
"""
import re
from functools import cache

INPUT_FILE = './resources/day12_input.txt'


def validate(line: str, numbers: list):
    """
    Validates the spring row if it matches with the group number combo

    Parameters:
    - line: spring row
    - numbers: group combo
    """
    return [len(spring) for spring in re.findall(r'#+', line)] == numbers


def open_file():
    def exfil_part1(line: str):
        return line.split(" ")[0], eval(line.split(" ")[1])

    def exfil_part2(line: str):
        springs = '?'.join([line.split(" ")[0]] * 5)
        group = tuple([int(n) for n in re.findall(r'\d+', line)] * 5)
        return springs, group

    return list(map(exfil_part1, open(INPUT_FILE, 'r'))), list(map(exfil_part2, open(INPUT_FILE, 'r')))

@cache # used for memomization
def permutate(springs: str, group: tuple):
    """
    Taken from another coder, added my own comments
    for later studying and my improvement of critical thinking
    .
    Credit: @Domyy95
    """
    if not group:  # if group numbers are empty, return 1 if no more '#' are found else 0
        return 1 if '#' not in springs else 0
    if not springs:  # if spring row is fully analyzed, return 1 if group numbers are empty, else 0
        return 1 if not group else 0

    result = 0
    if springs[0] in '.?':  # if first character of spring is '.' or '?', then recurse a starting from the second index
        result += permutate(springs[1:], group)

    if springs[0] in "#?":
        # if first character of spring is '#' or '?'
        if (
            # validate that the next numbers of '#' is within the length of springs
            group[0] <= len(springs)
            # no 'gaps' between first character and idx of where the '#' ends
            and "." not in springs[: group[0]]
            # number == len of springs OR idx of spring is not '#'
            and (group[0] == len(springs) or springs[group[0]] != "#")
        ):
            result += permutate(springs[group[0] + 1:], group[1:])

    return result

@cache
def count(springs: list, group: tuple):
    """
    Originally, this method was what I came up with
    but after seeing how slow it performs for both
    part 1 and part 2, i viewed other solutions to
    understand how to improve the runtime.
    """
    if '?' not in springs:
        return 1 if validate(''.join(springs), [n for n in group]) else 0

    idx = springs.index('?')

    springs[idx] = '#'  # first change
    first_recur = count(springs, group)

    springs[idx] = '.'  # second change
    second_recur = count(springs, group)

    springs[idx] = '?'  # back tracking
    return first_recur + second_recur


if __name__ == '__main__':
    s_data1, s_data2 = open_file()
    sum_1 = 0
    sum_2 = 0
    for i in s_data1:
        sum_1 += permutate(i[0], i[1])
        # sum_1 += count([c for c in i[0]], i[1])
    for i in s_data2:
        sum_2 += permutate(i[0], i[1])
        # sum_1 += count([c for c in i[0]], i[1])

    print(sum_1)
    print(sum_2)
