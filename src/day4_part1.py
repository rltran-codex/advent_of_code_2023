import re

INPUT_FILE = './resources/day4_input.txt'
"""
'card n' : {
  'winning_numbers' : {
    int : num_of_matches
  },
  'numbers_pulled' : [],
  'total_points' : int
}
"""
colorful_cards = {}


def calculate_points(matches: int):
    total_points = 0
    for i in range(matches):
        if i == 0:  # one point for first match
            total_points += 1
            continue
        total_points *= 2  # double the point of each match after the first match

    return total_points

def calculate_cards_total():
    sum_1 = 0
    for i in colorful_cards.keys():
        sum_1 += colorful_cards[i]['total_points']

    return sum_1

def process_scratch_card(card_info : str, card_num : int):
    """
    Method handles processing each scratch card.
      1) splits the string with delimiter ':' and '|'
      2) creates a dict of the winning numbers
      3) creates a list of numbers scratched
      4) iterates through numbers scratched and tries to increment the winning numbers
      5) calculates the total points
      6) stores the results into colorful_cards : dict
    """
    pattern = r'[:|]'
    card_set = re.split(pattern, card_info)
    # dict object for winning numbers
    winning_set = {int(key): 0 for key in card_set[1].split()}
    # list of numbers you have scatched to reveal
    numbers_scratched = [int(x) for x in card_set[2].split()]
    # count the matches
    for num in numbers_scratched:
        try:
            winning_set[num] += 1
        except Exception:
            pass
    
    # store the results
    colorful_cards[card_num] = {
        'winning_numbers' : winning_set,
        'numbers_pulled' : numbers_scratched,
        'total_points' : calculate_points(sum(winning_set.values()))
    }

def load_file():
    with open(INPUT_FILE, 'r') as file:
        lines = [line.strip() for line in file]
        for idx, c in enumerate(lines):
          process_scratch_card(c, idx + 1)

if __name__ == "__main__":
    sum_1 = 0
    load_file()
    sum_1 = calculate_cards_total()

    print(f"Part I answer: {sum_1}")