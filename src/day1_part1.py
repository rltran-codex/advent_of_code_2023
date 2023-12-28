"""
-- Part One --
Given calibration document consists of lines of text; each line originally 
contained a specific calibration value that the Elves now need to recover. 
On each line, the calibration value can be found by combining the first digit 
and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. 
Adding these together produces 142.
What is the sum of all of the calibration values?

Reference: https://adventofcode.com/2023/day/1
Author: Richard Tran
Status: Completed
"""
import re

INPUT_FILE = './resources/day1_input.txt'

sum = 0
calibration_values = []

if __name__ == "__main__":
    with open(INPUT_FILE, 'r') as f:  # open input file for processing
        content = [line.strip() for line in f]  # load each line into an array

        for c in content:  # iterate through each item in content
            # extract numbers from string
            extracted_nums = re.findall(r'\d', c)
            size = len(extracted_nums)
            value = ''.join([extracted_nums[0], extracted_nums[size - 1]])
            calibration_values.append(int(value))

    for c_val in calibration_values:
        sum += c_val

    print(f"Part I answer: {sum}")
