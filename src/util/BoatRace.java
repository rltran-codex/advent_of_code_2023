package util;

import java.util.HashMap;

/**
 * ! TODO - provide javadoc
 */
public class BoatRace {
  private long time;
  private long distance_record;
  private long btn_hold_min;
  private long btn_hold_max;
  private HashMap<Long, Long> calc_btn_hold;

  public BoatRace(int time, int distance_record) {
    this((long) time, (long) distance_record);
  }

  public BoatRace(long time, long distance_record) {
    this.time = time;
    this.distance_record = distance_record;
    this.btn_hold_min = Integer.MAX_VALUE;
    this.btn_hold_max = Integer.MIN_VALUE;
    this.calc_btn_hold = new HashMap<>();
  }

  /**
   * The naive way of finding the number of ways
   * to beat the distance record.
   * 
   * @return the total amount of ways to beat the record
   */
  public long findNumberOfOptions() {
    // calculate the button hold options
    for (long i = 0; i <= this.time; i++) {
      long dist = calculate_distance(i);
      if (dist > this.distance_record) {
        if (i > this.btn_hold_max) {
          this.btn_hold_max = i;
        }

        if (i < this.btn_hold_min) {
          this.btn_hold_min = i;
        }
        this.calc_btn_hold.put(i, dist);
      }
    }

    return numberOfOptions();
  }

  /**
   * This method optimizes finding the number of
   * options a player can do in order to beat the 
   * distance record. This method helps for
   * day 5 part II by using "dividing" and "binary search"
   * like algorithm to find the shortest time and 
   * longest time a button can be held.
   * 
   * When the calculated button hold and distance traveled
   * are graphed, the graph can be seen to create a parabola.
   * Thus, using the threshold of the record distance to beat,
   * we can quickly have a stopping condition.
   * 
   * @return the total amount of ways to beat the record
   */
  public long findOptimized() {
    long left_bnd = 0;
    long right_bnd = this.time;
    long mid_ptr = this.time / 2;

    left_bnd = evaluateLeftBoundary(mid_ptr);
    right_bnd = evaluateRightBoundary(mid_ptr);

    this.btn_hold_min = left_bnd;
    this.btn_hold_max = right_bnd;
    return right_bnd - left_bnd;
  }

  private long evaluateLeftBoundary(long mid_ptr) {
    long left = 0;
    long right = mid_ptr;
    long mid = 0;
    // search for the left bound of the parabola
    while (left <= right) {
      mid = left + (right - left) / 2;
      long left_calc = calculate_distance(mid);
      // if calculated is in the range of record distance +- 20%
      if (left_calc < this.distance_record) {
        left = mid + 1;
      } else if (left_calc > this.distance_record) {
        right = mid - 1;
      } else {
        // boundary found
        break;
      }
    }

    return mid;
  }

  private long evaluateRightBoundary(long mid_ptr) {
    long left = mid_ptr;
    long right = this.time;
    long mid = 0;
    while (left <= right) {
      mid = left + (right - left) / 2;
      long right_calc = calculate_distance(mid);
      // if calculated is in the range of record distance +- 20%
      if (right_calc < this.distance_record) {
        right = mid - 1;
      } else if (right_calc > this.distance_record) {
        left = mid + 1;
      } else {
        // boundary found
        break;
      }
    }

    return mid;
  }

  private long calculate_distance(long time_held) {
    if (time_held == 0 || time_held == this.time) {
      return 0;
    }

    return time_held * 1 * (this.time - time_held);
  }

  public int numberOfOptions() {
    return calc_btn_hold.size();
  }
}
