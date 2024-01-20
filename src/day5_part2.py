"""
-- Part II --
Note:
Initially, the solution worked for the sample input since the arrays created were small enough
to handle. However, using the actual puzzle input caused the program to take forever since
the data size was in the millions/billions. Thus, the solution was reworked to use
"splicing" but only with the start and ending boundaries.

Reference: https://adventofcode.com/2023/day/5

Author: Richard Tran
Status: Completed
"""

import time
from day5_part1 import INPUT_FILE, extract_conversion_mapping
import sys

c_map = {}  # conversion map

class Seed_Population:
    def __init__(self, seed_pop: tuple):
        self.seed_pop_range = seed_pop     # seed population range
        self.lowest_location = sys.maxsize  # this population's lowest location

    def convert_seed_to_location(self):
        """
        Converts from seed number -> location number

        Parameters:
            None

        Returns:
            None

        Description:
            Method starts from the initial seed number population range, then
            follows the basic conversion stages:
            seed number -> soil -> fertilizer -> water -> light -> temperature -> humidity -> location

            Since the problem only asks for the lowest location number, after converting to location the 
            lowest location for this population set is determined and set.
        """
        s_pop = (
            self.seed_pop_range[0], self.seed_pop_range[0] + self.seed_pop_range[1] - 1)
        converted_numbers = []
        converted_numbers.append(s_pop)

        # convert to soil
        self.process_conversion_step(
            converted_numbers, c_map["seed_to_soil"])
        # convert to fertilizer
        self.process_conversion_step(
            converted_numbers, c_map["soil_to_fertilizer"])
        # convert to water
        self.process_conversion_step(
            converted_numbers, c_map["fertilizer_to_water"])
        # convert to light
        self.process_conversion_step(
            converted_numbers, c_map["water_to_light"])
        # convert to temperature
        self.process_conversion_step(
            converted_numbers, c_map["light_to_temperature"])
        # convert to humidity
        self.process_conversion_step(
            converted_numbers, c_map["temperature_to_humidity"])
        # convert to location
        self.process_conversion_step(
            converted_numbers, c_map["humidity_to_location"])

        # at this point, all seed numbers are converted to location numbers
        for i in converted_numbers:
            if i[0] < self.lowest_location:
                self.lowest_location = i[0]
        pass

    def process_conversion_step(self, before_conversion: list, conversions: list):
        """
        Converts a list of source categories to the destination category.

        Parameters:
            - before_conversion (list): A list of tuples with their source start and source end.
                Example: [(79, 92)]
            - conversions (list): A list of tuples representing the mapping.
                Example: If converting from seed-to-soil
                [(50, 98, 2), (52, 50, 48)]

        Returns:
            list: A list of tuples containing the ranges of the converted values.

        Description:
            This method is designed to convert source categories to the destination category.
            The 'before_conversion' parameter is a list of tuples representing the source categories to be converted.
            The 'conversions' parameter is a list of tuples representing the mapping rules.
            The method returns a list of tuples containing the ranges of the converted values.

            Note: The method was reworked to use range boundaries for splicing, addressing inefficiencies with enormous datasets.
        """
        converted_list = []
        for map in conversions:
            if not before_conversion:  # temp list is empty now
                break
            for idx, s in enumerate(before_conversion):
                r = self._check_boundaries(s[0], s[1], map)
                if r:
                    # remove number range since it will be split and converted
                    s_pop = before_conversion.pop(idx)

                    starting_index = r[0]
                    ending_index = r[1]

                    # add converted range to converted_list
                    converted_list.append((r[2], r[3]))
                    # splice "list" and store any unprocessed ones into temp_lists
                    left_splice = (s_pop[0], starting_index - 1)
                    right_splice = (ending_index + 1, s_pop[1])

                    # add splices to before_conversion if and only if range is valid:
                    # - left bound != right bound
                    # - left bound is less than right bound
                    if left_splice[0] != left_splice[1] and left_splice[0] < left_splice[1]:
                        before_conversion.append(left_splice)
                    if right_splice[0] != right_splice[1] and right_splice[0] < right_splice[1]:
                        before_conversion.append(right_splice)

        # add back the converted numbers to the before_conversion list
        for i in converted_list:
            before_conversion.append(i)

    def _check_boundaries(self, src_left, src_right, conversion: tuple):
        """
        Check boundaries for seed number conversion.

        Parameters:
            - src_left (int): Left boundary of the source seed number range.
            - src_right (int): Right boundary of the source seed number range.
            - conversion (tuple): A tuple representing the conversion parameters.
                - conversion[0] (int): Start point of the destination category.
                - conversion[1] (int): Start point of the source category.
                - conversion[2] (int): Length of the conversion range.

        Returns:
            tuple or None: A tuple representing the range to convert or None if the conversion is outside of the seed number range.
            range_to_convert (tuple): representing the range to convert and splice
            - range_to_convert[0] (int): starting source bound
            - range_to_convert[1] (int): ending source bound
            - range_to_convert[2] (int): calculated destination start
            - range_to_convert[3] (int): calculated destination end


        Description:
            The method checks if the conversion range is within the boundaries of the given source range.
            If the conversion range is within the range, it calculates the corresponding range for conversion.
            Returns None if the conversion is outside of the range.
        """
        # marking beginning and end of seed numbers
        s_pop_start = src_left
        s_pop_end = src_right

        start_point = conversion[1]                     # src_category start
        end_point = start_point + conversion[2] - 1     # src_category end

        dest_start = conversion[0]                      # dest_category start
        dest_end = conversion[2] + dest_start - 1       # dest_category end
        diff = dest_start - start_point
        # check if conversion range is outside of seed number range
        if ((end_point < s_pop_start) or
                (start_point > s_pop_end)):
            return None

        range_to_convert = ()
        # case: conversion subset is on the left
        if start_point <= s_pop_start and s_pop_start <= end_point <= s_pop_end:
            range_to_convert = (s_pop_start, end_point,
                                s_pop_start + diff, end_point + diff)
        # case: conversion subset is in the middle
        elif s_pop_start <= start_point <= s_pop_end and s_pop_start <= end_point <= s_pop_end:
            range_to_convert = (start_point, end_point,
                                start_point + diff, end_point + diff)
        # case: conversion subset is on the right
        elif s_pop_start <= start_point <= s_pop_end and s_pop_end <= end_point:
            range_to_convert = (start_point, s_pop_end,
                                start_point + diff, s_pop_end + diff)
        # case: convert the entire array of seed numbers
        elif start_point <= s_pop_start <= end_point and start_point <= s_pop_end <= end_point:
            range_to_convert = (s_pop_start, s_pop_end,
                                s_pop_start + diff, s_pop_end + diff)

        return range_to_convert


def extract_seed_numbers() -> list:
    """
    Method opens the puzzle input and
    extracts the seed numbers and its respective range.
    Adds each item into a list and returns it after completing the
    process.
    """
    with open(INPUT_FILE, 'r') as file:
        content = file.read().splitlines()
        seeds = [int(s_num) for s_num in content[0].split(":")[1].split()]
        idx = 0
        s_list = []  # store as tuples instead
        while idx < len(seeds) - 1:
            s_list.append((seeds[idx], seeds[idx + 1]))
            idx += 2
        s_list.sort()

        seed_populations = []
        for s_pop in s_list:
            seed_populations.append(Seed_Population(s_pop))

    return seed_populations


def find_lowest_location(seed_population: list) -> int:
    """
    Method iterates through the list of Seed_Populations objects
    and converts seed number to location.

    After each convert_seed_to_location(), the method changes
    the object's lowest location number
    """
    lowest_num = sys.maxsize
    for i in seed_population:
        i.convert_seed_to_location()
        if i.lowest_location < lowest_num:
            lowest_num = i.lowest_location

    return lowest_num


if __name__ == "__main__":
    start = time.time_ns()
    # initialize by opening file and extracting seed numbers and conversion maps
    seed_objects = extract_seed_numbers()
    c_map = extract_conversion_mapping()
    # sort the conversion mappings
    for i in c_map:
        c_map[i].sort()
        pass

    end = time.time_ns()
    lowest_loc = find_lowest_location(seed_objects)
    print(f"Part II answer: {lowest_loc}")
    print(f"Time: {(end - start)} ns")
