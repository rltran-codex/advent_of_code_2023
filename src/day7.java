import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

import util.CamelCardHand;
import util.InputFileUtil;
import util.CamelCardHand.HAND_TYPE;

public class day7 {
  private static final String INPUT_FILE = "./resources/day7_input.txt";

  public static HashMap<HAND_TYPE, ArrayList<CamelCardHand>> partOne() {
    List<String> file_input = InputFileUtil.open_file(INPUT_FILE);

    // initialize map where the hand type is the key and the list of hands are the values.
    HashMap<HAND_TYPE, ArrayList<CamelCardHand>> hand_type_map = new HashMap<>();
    for (HAND_TYPE value : HAND_TYPE.values()) {
      hand_type_map.put(value, new ArrayList<>());
    }

    // read file and create CamelCardHand objects, adding them to the respective hashmap key
    for (String line : file_input) {
      String[] split = line.split((" "));

      if (split.length != 2) {
        continue;
      }

      try {
        CamelCardHand camelHand = new CamelCardHand(split[0], split[1], 1);
        hand_type_map.get(camelHand.hand_type).add(camelHand);
      } catch (Exception e) {
        System.err.println(e.getMessage());
      }
      
      // Iterate through each rank and sort the array list based on their strength
      hand_type_map.forEach((key, value) -> {
        Collections.sort(value);
      });
    }

    return hand_type_map;
  }
  
  public static HashMap<HAND_TYPE, ArrayList<CamelCardHand>> partTwo() {
    List<String> file_input = InputFileUtil.open_file(INPUT_FILE);

    // initialize map where the hand type is the key and the list of hands are the values.
    HashMap<HAND_TYPE, ArrayList<CamelCardHand>> hand_type_map = new HashMap<>();
    for (HAND_TYPE value : HAND_TYPE.values()) {
      hand_type_map.put(value, new ArrayList<>());
    }

    // read file and create CamelCardHand objects, adding them to the respective hashmap key
    for (String line : file_input) {
      String[] split = line.split((" "));

      if (split.length != 2) {
        continue;
      }

      try {
        CamelCardHand camelHand = new CamelCardHand(split[0], split[1], 2);
        hand_type_map.get(camelHand.hand_type).add(camelHand);
      } catch (Exception e) {
        System.err.println("FAILED AT " + line);
        // System.err.println(e.getMessage());
      }
      
      // Iterate through each rank and sort the array list based on their strength
      hand_type_map.forEach((key, value) -> {
        Collections.sort(value);
      });
    }

    return hand_type_map;
  }

  public static void processWinningCalculations(HashMap<HAND_TYPE, ArrayList<CamelCardHand>> hand_type_map) {
    // flatten the hashmap into an array that resembles the ranking of each hand
    ArrayList<CamelCardHand> rank = new ArrayList<>();
    for (HAND_TYPE h : HAND_TYPE.values()) {
      if (hand_type_map.get(h).isEmpty()) {
        continue;
      }

      List<CamelCardHand> temp = hand_type_map.get(h);
      temp.forEach(e -> rank.add(e));
    }
    
    // finally, add up the sum of winnings
    int winnings = 0;
    for (int i = 0; i < rank.size(); i++) {
      CamelCardHand e = rank.get(i);
      int rank_num = i + 1;
      winnings += rank_num * e.bid_amt;
      // Uncomment below to list all ranks and hand info
      // System.out.printf("{Rank = %5d} : {Cards = %-20s} : {Bid = %5s} : {Type = %15s} : {Winnings = %8d}\n", rank_num, Arrays.toString(e.cards_encoded), e.bid_amt, e.hand_type, e.bid_amt * rank_num);
    }
    System.out.printf("Total Winnings: %d\n", winnings);
  }
  public static void main(String[] args) {
    HashMap<HAND_TYPE, ArrayList<CamelCardHand>> p1_rank = partOne();
    HashMap<HAND_TYPE, ArrayList<CamelCardHand>> p2_rank = partTwo();

    processWinningCalculations(p1_rank);
    processWinningCalculations(p2_rank);
  }
}
