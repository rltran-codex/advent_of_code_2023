"""
-- Part Two -- 
Some of the digits are actually spelled out with letters: 
one, two, three, four, five, six, seven, eight, and nine
also count as valid "digits".

Equipped with this new information, you now need to find the real first and last 
digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

Reference: https://adventofcode.com/2023/day/1
Author: Richard Tran
Status: Completed
"""
import re

INPUT_FILE = './resources/day1_input.txt'
NUMBER_STRING = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

# (?=(one | two | three | four | five | six | seven | eight | nine | [0-9]))
REGEX_PATTERN = re.compile(
    fr'(?=({"|".join([key for key in NUMBER_STRING])}|[0-9]))', re.IGNORECASE)


def refactor_list(extracted: list) -> list:
    """
    Method iterates through an extracted list and changes it to the value accordingly.
    Ex:
    refactor_list(["eight", "5", "nine"]) -> ["8", "5", "9"]
    """
    new_list = []
    for val in extracted:
        num = NUMBER_STRING.get(val)
        if num:
            val = num

        new_list.append(val)

    return new_list


if __name__ == "__main__":
    calibration_values = []
    with open(INPUT_FILE, 'r') as f:  # open input file for processing
        content = [line.strip() for line in f]  # load each line into an array

        for c in content:  # iterate through each item in content
            # must check matches where matches overlap. EX: oneight -> [1, 8]
            results = [match.group(1)
                       for match in re.finditer(REGEX_PATTERN, c)]
            # PART II: change all occurance of number strings to number
            extracted_nums = refactor_list(results)
            size = len(extracted_nums)
            value = ''.join([extracted_nums[0], extracted_nums[size - 1]])
            calibration_values.append(int(value))

    sum = 0
    for c_val in calibration_values:
        sum += c_val

    print(f'Part II answer: {sum}')
