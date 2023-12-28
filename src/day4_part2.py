import day4_part1 as day4

day4.load_file()  # load the file and populate day4.colorful_cards
cards_owned = {key: 0 for key in day4.colorful_cards.keys()}


def award_cards(winning_numbers: dict, card_num: int, num_of_copies: int):
    """
    Award cards based on the provided winning numbers and card information.
    Parameters:
    - winning_numbers (dict): A dictionary representing the winning numbers match.
    - card_num (int): The card number for which awards are calculated.
    - num_of_copies (int): The number of copies of the card that are present.
    The method calculates the total matches in the winning numbers and increments
    the count of awarded cards for each matching number, multiplied by the
    specified number of copies.
    """
    total = 0
    for i in winning_numbers:
        total += winning_numbers[i]

    if total == 0:
        return

    for i in range(1, total + 1):
        if card_num + i in cards_owned:
            cards_owned[card_num + i] += num_of_copies

    return


if __name__ == "__main__":
    scratch_cards = day4.colorful_cards
    sum_2 = 0

    # initially the number of cards we own is 0. Thus each iteration we add one since its in the puzzle input
    for card_num in scratch_cards.keys():
        cards_owned[card_num] += 1
        num_of_copies = cards_owned[card_num]
        award_cards(scratch_cards[card_num]
                    ['winning_numbers'], card_num, num_of_copies)

        sum_2 += cards_owned[card_num]

    print(f"Part II answer: {sum_2}")
