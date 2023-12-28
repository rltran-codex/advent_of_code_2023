"""
-- Part 1 --
Given a record of games (puzzle input), that contain game ID and each pull result separated by a semicolon.
Ex:
  Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
  Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
  Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
  Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
  Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

If a game consists of a pull result that exceeds the threshold, then the game is invalid.
Determine which games would have been possible if the bag had been loaded with 
only 12 red cubes, 13 green cubes, and 14 blue cubes. 
What is the sum of the IDs of those games?

-- Part 2 --
Using the same record of games, what is the fewest number of cubes of each color
that could have been inthe bag to make the game possible? Thus, what is the total
MAXIMUM number of each color that can be present for the game to generate the pull results
in the game.

Ex:
  Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
  Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
  Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
  Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
  Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    - In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
    - Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
    - Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
    - Game 4 required at least 14 red, 3 green, and 15 blue cubes.
    - Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

For each game, find the minimum set of cubes that must have been present.
What is the sum of the power of these sets?

Reference: https://adventofcode.com/2023/day/2

Author: Richard Tran
Status: Completed
"""
import re
import sys

INPUT_FILE = './resources/day2_input.txt'

RED_REGEX = r'(\d+)red'
BLUE_REGEX = r'(\d+)blue'
GREEN_REGEX = r'(\d+)green'

NUM_CUBE_THRESHOLD = {
    'red': 12,
    'blue': 14,
    'green': 13
}

sum_1 = 0
sum_2 = 0


class Game_Record:

    def __init__(self, record: str):
        game_info = record.split(':')
        self.game_id = int(re.findall(r'\d+', game_info[0])[0])
        self.valid_config, self.cubed_min = self._process_pull_results(
            game_info[1])

    def _process_pull_results(self, game_log: str) -> bool:
        pulls = game_log.replace(' ', '').split(';')
        valid = True
        red_cubes = -sys.maxsize
        blu_cubes = -sys.maxsize
        gre_cubes = -sys.maxsize

        for pull_result in pulls:
            red_matches = self._retrieve_color_count(RED_REGEX, pull_result)
            blue_matches = self._retrieve_color_count(BLUE_REGEX, pull_result)
            green_matches = self._retrieve_color_count(
                GREEN_REGEX, pull_result)

            # if any color in this pull result exceeds the threshold, game is invalid
            if red_matches > NUM_CUBE_THRESHOLD['red']:
                valid = False
            if blue_matches > NUM_CUBE_THRESHOLD['blue']:
                valid = False
            if green_matches > NUM_CUBE_THRESHOLD['green']:
                valid = False

            if red_matches > red_cubes:
                red_cubes = red_matches
            if blue_matches > blu_cubes:
                blu_cubes = blue_matches
            if green_matches > gre_cubes:
                gre_cubes = green_matches

        # if code has gotten to this point, then all pulls in current Game is valid
        return valid, (red_cubes * blu_cubes * gre_cubes)

    def _retrieve_color_count(self, match: str, pull_result: str) -> int:
        count = 0
        try:
            count = int(re.findall(match, pull_result)[0])
        except IndexError:
            pass

        return count


if __name__ == "__main__":
    with open(INPUT_FILE, 'r') as file:
        game_records = [input_line for input_line in file]
        for game in game_records:
            g = Game_Record(game)
            if g.valid_config:
                sum_1 += g.game_id

            sum_2 += g.cubed_min

        print(f"Part I  answer: {sum_1}")
        print(f"Part II answer: {sum_2}")
