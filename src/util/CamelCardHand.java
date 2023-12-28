package util;

import java.util.HashMap;
import java.util.Map;

/**
 * CamelCardHand object represents a hand of cards for the game, Camel Cards.
 * Provides methods for encoding the hand, building a card map, and calculating
 * the hand type.
 */
public class CamelCardHand implements Comparable<CamelCardHand> {
  public int bid_amt;
  public Integer[] cards_encoded;
  public Integer[] joker_buff; // used for Part II where J are wildcards that can act like whatever card would
                               // make the hand the strongest type
  private HashMap<Integer, Integer> card_map;
  public HAND_TYPE hand_type;

  /**
   * Constructs a CamelCardHand object with the specified hand and bid.
   *
   * @param hand A string representation of the hand.
   * @param bid  A string representation of the bidding amount.
   * @throws Exception             If an invalid number of cards is found in the
   *                               hand.
   * @throws NumberFormatException If the bidding amount cannot be parsed as an
   *                               integer.
   */
  public CamelCardHand(String hand, String bid, int part) throws Exception, NumberFormatException {
    switch (part) {
      case 1:
        this.cards_encoded = encodeCards1(hand.split("")); // convert cards from String to Integer
        this.card_map = buildCardMap();
        break;
      case 2:
        // if J is found in the hand, calculate the Joker Buff
        this.cards_encoded = encodeCards2(hand.split("")); // convert cards from String to Integer
        this.card_map = buildCardMap();
        encodeJokerBuff();
        break;
      default:
        break;
    }

    this.bid_amt = Integer.parseInt(bid);
    this.hand_type = calculateHandType();
  }

  /**
   * Encodes an array of card strings into an array of corresponding integer
   * values for Part I.
   *
   * @param cards Array of card strings to be encoded.
   * @return Array of encoded card values.
   */
  private Integer[] encodeCards1(String[] cards) {
    Integer[] c_encode = new Integer[cards.length];
    HashMap<String, Integer> card_rank = new HashMap<>() {
      {
        put("A", 15);
        put("K", 14);
        put("Q", 12);
        put("J", 11);
        put("T", 10);
        put("9", 9);
        put("8", 8);
        put("7", 7);
        put("6", 6);
        put("5", 5);
        put("4", 4);
        put("3", 3);
        put("2", 2);
      }
    };

    for (int i = 0; i < cards.length; i++) {
      c_encode[i] = card_rank.get(cards[i]);
    }

    return c_encode;
  }

  /**
   * Encodes an array of card strings into an array of corresponding integer
   * values for Part II.
   * 
   * @param cards
   * @return
   */
  private Integer[] encodeCards2(String[] cards) {
    Integer[] c_encode = new Integer[cards.length];
    HashMap<String, Integer> card_rank = new HashMap<>() {
      {
        put("A", 15);
        put("K", 14);
        put("Q", 12);
        put("T", 10);
        put("9", 9);
        put("8", 8);
        put("7", 7);
        put("6", 6);
        put("5", 5);
        put("4", 4);
        put("3", 3);
        put("2", 2);
        put("J", 1);
      }
    };

    for (int i = 0; i < cards.length; i++) {
      c_encode[i] = card_rank.get(cards[i]);
    }

    return c_encode;
  }

  /**
   * Joker cards can pretend to be whatever card is best
   * to become a better type of hand. However, Joker cards
   * are treated to be the weakest card. 
   * Ex:
   * QJJQ2 is now considered four of a kind.
   * QJJQK2 is weaker than QQQQ2 since J is weaker than Q.
   */
  private void encodeJokerBuff() {
    // if no jokers are present, return
    if (!card_map.containsKey(1)) {
      return;
    }
    
    int highest_count = Integer.MIN_VALUE;
    int highest_card = Integer.MIN_VALUE;
    int num_of_jokers = card_map.get(1);

    // if hand consists of five jokers, then return
    if (num_of_jokers == 5) {
      return;
    }
    
    this.card_map.remove(1);
    
    // identify the card that has the most count
    for (Map.Entry<Integer, Integer> entry : this.card_map.entrySet()) {
      int card = entry.getKey();
      int count = entry.getValue();

      // continue if:
      // - card count is not the highest
      // - card count is equal and not the highest card
      if (!(highest_count < count) && !(highest_count == count && highest_card < card)) {
        continue;
      }
      highest_count = count;
      highest_card = card;
    }

    // increment the highest card with the number of jokers present
    this.card_map.put(highest_card, highest_count + num_of_jokers);
  }

  /**
   * Method iterates through the array of encoded
   * cards and maps the card values with their
   * respective number of occurance.
   * 
   * @return HashMap containg card values and their counts
   *
   */
  private HashMap<Integer, Integer> buildCardMap() {
    if (this.cards_encoded == null) {
      return null;
    }

    HashMap<Integer, Integer> nMap = new HashMap<>();
    // iterate over the array of cards
    for (Integer card : this.cards_encoded) {
      if (nMap.containsKey(card)) {
        nMap.put(card, nMap.get(card) + 1);
      } else {
        nMap.put(card, 1);
      }
    }

    return nMap;
  }

  /**
   * Method uses the HashMap to calculate the type.
   * 
   * @return HAND_STRENGTH enum
   * @throws Exception If an invalid number of cards is found in the hand.
   */
  private HAND_TYPE calculateHandType() throws Exception {
    /*
     * check the type of hand
     * -- five of a kind - card_map size = 1 and count = 5
     * -- four of a kind - card_map size = 2 and card x = 4, card y = 1
     * -- full house - card_map size = 2 and card x = 3, card y = 2
     * -- three of a kind - card_map size = 3 and card x = 3, card y = 1, card z = 1
     * -- two pair - card_map size = 3, card x = 2, card y = 2, card z = 1
     * -- one pair - card_map size = 4, card x = 2, card y = 1, card z = 1, card t =
     * 1
     * -- high card - card_map size = 5, all cards are distinct
     */
    int card_x = 0;
    int card_y = 0;
    int card_z = 0;
    int n = 0;
    HAND_TYPE type = null;

    for (Map.Entry<Integer, Integer> entry : this.card_map.entrySet()) {
      switch (n) {
        case 0:
          card_x = entry.getValue();
          break;
        case 1:
          card_y = entry.getValue();
          break;
        case 2:
          card_z = entry.getValue();
          break;
        default:
          break;
      }

      n++;
    }

    switch (this.card_map.size()) {
      case 1:
        if (card_x == 5) {
          type = HAND_TYPE.five_of_a_kind;
        }
        break;
      case 2:
        if (card_x == 4 || card_y == 4) {
          type = HAND_TYPE.four_of_a_kind;
        } else if (card_x == 3 || card_y == 3) {
          type = HAND_TYPE.full_house;
        }
        break;
      case 3:
        if ((card_x == 3 || card_x == 1) &&
            (card_y == 3 || card_y == 1) &&
            (card_z == 3 || card_z == 1)) {
          type = HAND_TYPE.three_of_a_kind;
        } else if ((card_x == 2 || card_x == 1) &&
            (card_y == 2 || card_y == 1) &&
            (card_z == 2 || card_z == 1)) {
          type = HAND_TYPE.two_pair;
        }
        break;
      case 4:
        type = HAND_TYPE.one_pair;
        break;
      case 5:
        type = HAND_TYPE.high_card;
        break;
      default:
        throw new Exception("Invalid number of cards found in this hand: " + this.cards_encoded);
    }

    return type;
  }

  @Override
  public int compareTo(CamelCardHand o) {
    int size = this.cards_encoded.length;
    int result = 0;

    for (int i = 0; i < size; i++) {
      int compare_1 = this.cards_encoded[i];
      int compare_2 = o.cards_encoded[i];

      if (compare_1 == compare_2) {
        continue;
      } else if (compare_1 < compare_2) {
        result = -1;
      } else {
        result = 1;
      }
      break;
    }

    return result;
  }

  /**
   * Enum representing the possible hand type of a CamelCardHand.
   */
  public enum HAND_TYPE {
    high_card(2),
    one_pair(3),
    two_pair(4),
    three_of_a_kind(5),
    full_house(6),
    four_of_a_kind(7),
    five_of_a_kind(8);

    public final int points;

    private HAND_TYPE(int points) {
      this.points = points;
    }
  }
}
