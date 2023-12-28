package util;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class InputFileUtil {
  public static List<String> open_file(String puzzle_input) {
    List<String> lines = new ArrayList<>();

    try {
      BufferedReader b_reader = new BufferedReader(new FileReader(puzzle_input));
      String line;

      while ((line = b_reader.readLine()) != null) {
        lines.add(line);
      }

      b_reader.close();
    } catch (IOException e) {
      return null;
    }

    return lines;
  }
}
