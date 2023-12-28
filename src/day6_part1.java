import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import util.BoatRace;

/**
 * ! TODO - provide javadoc
 */
public class day6_part1 {
  private static final String INPUT_FILE = "./resources/day6_input.txt";
  private static List<BoatRace> races = new ArrayList<>();

  public static void open_file() {
    ArrayList<Integer> time_vals = null;
    ArrayList<Integer> distance_vals = null;

    try {
      BufferedReader b_reader = new BufferedReader(new FileReader(INPUT_FILE));
      String line;

      while ((line = b_reader.readLine()) != null) {
        // if line doesn't start with Time or Distance, read next line
        if (line.startsWith("Time")) {
          time_vals = extract_numbers(line);
        }

        if (line.startsWith("Distance")) {
          distance_vals = extract_numbers(line);
        }
      }

      b_reader.close();
    } catch (IOException e) {
      System.err.println(e.getMessage());
    }


    // if opening file was unsuccessful, exit program
    if (time_vals == null || distance_vals == null) {
      System.exit(-1);
    }

    // if sizes don't match, exit program
    if (time_vals.size() != distance_vals.size()) {
      System.exit(-1);
    }

    // Create BoatRace obj and add to list of races
    int size = time_vals.size();
    for (int i = 0; i < size; i++) {
      BoatRace nRace = new BoatRace(time_vals.get(i), distance_vals.get(i));
      races.add(nRace);
    }
  }

  private static ArrayList<Integer> extract_numbers(String line) {
    // process numbers in the line
    String[] category = line.split(":");
    if (category.length != 2) {
      return null;
    }

      String[] numbers_extracted = category[1].split("\\s+");
      ArrayList<Integer> numbers = new ArrayList<>() {
        {
          for (String num : numbers_extracted) {
            try {
              add(Integer.parseInt(num));
            } catch (NumberFormatException e) {
            }
          }
        }
      };

      return numbers;
    }

  public static void main(String[] args) {
    open_file();
    int multiplied_sum = 1;
    for (BoatRace br : races) {
      multiplied_sum *= br.findNumberOfOptions();
    }

    String msg = String.format("Part I answer: %d", multiplied_sum);
    System.out.println(msg);
  }
}