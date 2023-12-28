import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import util.InputFileUtil;

/**
 * day9 contains solutions to both part 1 and part 2.
 * 
 * Post notes:
 * The repetitive iteration of the puzzle can be seen as a
 * recursive problem since we start by making a new sequence 
 * from the difference at each step of your history until
 * all zeroes are present in the array.
 * Then, we extrapolate backwards.
 * 
 * Refer to sumOfRight for the recusive algorithm
 * The right side of the "Triangle" we add the bottom row's extrapolated
 * value with the last value in the current row. For example:
 * 0   3   6   9  12  15   B
 *   3   3   3   3   3   A
 *     0   0   0   0   0
 * B = 15 - A
 * 
 * Refer to sumOfLeft for the recusive algorithm
 * The left side of "Triangle" we subtract the previous row's first value
 * with the first value of the current row:
 * B   3   6   9  12  15   x
 *   A   3   3   3   3   x
 *     0   0   0   0   0
 * 
 * B = 3 - A
 */
public class day9 {
  
  private static final String INPUT_FILE = "./resources/day9_input.txt";
  private static HashMap<Integer, Integer[]> history_map;

  public static void partOne() {
    int sum = 0;
    for (Map.Entry<Integer, Integer[]> entry : history_map.entrySet()) {
      Integer[] curr_history = entry.getValue();
      sum += sumOfRight(Arrays.copyOf(curr_history, curr_history.length + 1));
    }
    
    System.out.println("Part 1 answer: " + sum);
  }
  
  public static void partTwo() {
    int sum = 0;
    for (Map.Entry<Integer, Integer[]> entry : history_map.entrySet()) {
      Integer[] curr_history = entry.getValue();
      sum += sumOfLeft(Arrays.copyOf(curr_history, curr_history.length + 1));
    }

    System.out.println("Part 2 answer: " + sum);
  }

  /**
   * Recursive algorithm to extrapolate values from a given
   * history on the right side. Part I solution
   * 
   * @param arr - history line
   * @return extrapolated value at arr[length - 1]
   */
  private static int sumOfRight(Integer[] arr) {
    if (isRowZerod(arr)) { // base case
      arr[arr.length - 1] = 0;
      return arr[arr.length - 1];
    }

    Integer[] next_row = new Integer[arr.length - 1];
    for (int i = 0; i < arr.length - 2; i++) {
      next_row[i] = arr[i + 1] - arr[i];
    }
    int add_me = sumOfRight(next_row);
    arr[arr.length - 1] = arr[arr.length - 2] + add_me;
    return arr[arr.length - 1];
  }

  /**
   * Recursive algorithm to extrapolate values from a given
   * history on the left side. Part II solution.
   * @param arr
   * @return
   */
  private static int sumOfLeft(Integer[] arr) {
    if (isRowZerod(arr)) { // base case
      return 0;
    }

    Integer[] next_row = new Integer[arr.length - 1];
    for (int i = 0; i < arr.length - 2; i++) {
      next_row[i] = arr[i + 1] - arr[i];
    }
    next_row[0] = sumOfLeft(next_row);
    arr[0] = arr[0] - next_row[0];  // modified for part II of day 8
    return arr[0];
  }

  /**
   * Method to check the array to see if the 
   * current row is zero. 
   * Does not check the last index since it is
   * the extrapolated value.
   * 
   * @param arr
   * @return
   */
  private static boolean isRowZerod(Integer[] arr) {
    for (int i = 0; i < arr.length - 2; i++) {
      if (arr[i] != 0) {
        return false;
      }
    }

    return true;
  }

  private static void init() {
    history_map = new HashMap<>();
    List<String> histories = InputFileUtil.open_file(INPUT_FILE);
    for (int i = 0; i < histories.size(); i++) {
      String[] split = histories.get(i).split(" ");
      Integer[] history = new Integer[split.length];

      for (int num = 0; num < split.length; num++) {
        history[num] = Integer.parseInt(split[num]);
      }

      history_map.put(i, history);
    }
  }

  public static void main(String[] args) {
    init();
    partOne();
    partTwo();
  }
}
