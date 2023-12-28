"""
-- Part I --
Given an Almanac (puzzle input), determine the soil, fertilizer, water, light, temperature, and humidity
for each seed by using the mapping to convert from value to the next.
The conversion mapping is structured like:
(source category, destination category, range)
As an example, when converting from seed -> soil using:

  seeds: 79

  seed-to-soil map:
  50 98 2
  52 50 48 <-

Second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. 
This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. 
So, seed number 53 corresponds to soil number 55.
Using the destination category as a way to identify what seed number cooresponds with which soil, 
seed number 79 is determined to be mapped to 81.
Any source numbers that aren't mapped correspond to the same destination number.
So, seed number 10 corresponds to soil number 10.

Reference: https://adventofcode.com/2023/day/5

Author: Richard Tran
Status: Completed
"""
from sys import maxsize

INPUT_FILE = "./resources/day5_input.txt"
seed_map = {}
conversion_map = {}


def process_mapping(number: int, map:list) -> int:
    """
    number: the number to check in dest_category
    map: list of tuples(src_category:int, dest_category:int, range:int)
    """
    result = number
    for tuple in map:
        src_category = tuple[0]
        dest_category = tuple[1]
        r = tuple[2]

        if dest_category <= number <= (dest_category + r):
            result = src_category + (number - dest_category)
            break
    
    return result


def extract_seed_numbers():
    """
    Method extracts the seed numbers from the puzzle input
    
    """
    with open(INPUT_FILE, 'r') as file:
        content = file.read().splitlines()
        seeds = [int(s_num) for s_num in content[0].split(":")[1].split()]  # extract seed numbers
        seeds.sort() # sort seed numbers in ascending order
        # initialize seed_map
        seed_map = {key: {
            "soil": 0,
            "fertilizer": 0,
            "water": 0,
            "light": 0,
            "temperature": 0,
            "humidity": 0,
            "location": 0
        } for key in seeds}

        return seed_map

def extract_conversion_mapping():
    """
    Method extracts the list of maps from the puzzle input
    and returns a dictionary.

    returns:
    conversion_map = {
            "seed_to_soil": [],
            "soil_to_fertilizer": [],
            "fertilizer_to_water": [],
            "water_to_light": [],
            "light_to_temperature": [],
            "temperature_to_humidity": [],
            "humidity_to_location": []n
        }
    """
    with open(INPUT_FILE, 'r') as file:
        content = file.read().splitlines()
        seed_to_soil = []
        soil_to_fertilizer = []
        fertilizer_to_water = []
        water_to_light = []
        light_to_temperature = []
        temperature_to_humidity = []
        humidity_to_location = []

        parsing_state = None
        for line in content[1:]:
            if line.startswith("seed-to-soil map"):
                parsing_state = 0
                continue
            elif line.startswith("soil-to-fertilizer map"):
                parsing_state = 1
                continue
            elif line.startswith("fertilizer-to-water map"):
                parsing_state = 2
                continue
            elif line.startswith("water-to-light map"):
                parsing_state = 3
                continue
            elif line.startswith("light-to-temperature map"):
                parsing_state = 4
                continue
            elif line.startswith("temperature-to-humidity map"):
                parsing_state = 5
                continue
            elif line.startswith("humidity-to-location map"):
                parsing_state = 6
                continue
              

            # process line and split into a tuple of integers
            # (src_category, dest_category, range)
            mapping = tuple([int(num) for num in line.strip().split()])
            if mapping:
                match(parsing_state): # append to proper list based on parsing state
                    case 0:
                        seed_to_soil.append(mapping)
                    case 1:
                        soil_to_fertilizer.append(mapping)
                    case 2:
                        fertilizer_to_water.append(mapping)
                    case 3:
                        water_to_light.append(mapping)
                    case 4:
                        light_to_temperature.append(mapping)
                    case 5:
                        temperature_to_humidity.append(mapping)
                    case 6:
                        humidity_to_location.append(mapping)
                    case _:
                        continue

        conversion_map = {
            "seed_to_soil": seed_to_soil,
            "soil_to_fertilizer": soil_to_fertilizer,
            "fertilizer_to_water": fertilizer_to_water,
            "water_to_light": water_to_light,
            "light_to_temperature": light_to_temperature,
            "temperature_to_humidity": temperature_to_humidity,
            "humidity_to_location": humidity_to_location
        }
        
        return conversion_map

if __name__ == "__main__":
    seed_map = extract_seed_numbers()
    conversion_map = extract_conversion_mapping()
    for seed in seed_map.keys():
        soil  = process_mapping(seed,  conversion_map["seed_to_soil"])
        fert  = process_mapping(soil,  conversion_map["soil_to_fertilizer"])
        water = process_mapping(fert,  conversion_map["fertilizer_to_water"])
        light = process_mapping(water, conversion_map["water_to_light"])
        temp  = process_mapping(light, conversion_map["light_to_temperature"])
        hum   = process_mapping(temp,  conversion_map["temperature_to_humidity"])
        loc   = process_mapping(hum,   conversion_map["humidity_to_location"])

        # update seed mapping
        seed_map[seed].update({
            "soil": soil,
            "fertilizer": fert,
            "water": water,
            "light": light,
            "temperature": temp,
            "humidity": hum,
            "location": loc
        })

    # determine the lowest location number
    lowest_seed = maxsize
    lowest_loc = maxsize
    for seed in seed_map:
        loc_num = seed_map[seed]["location"]
        if loc_num < lowest_loc:
            lowest_loc = loc_num
            lowest_seed = seed
    
    print(f"Seed Number: {lowest_seed}")
    print(f"Location Number:{lowest_loc}")
