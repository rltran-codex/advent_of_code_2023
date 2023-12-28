
import util.InputFileUtil;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Day 8 of Advent of Code.
 * This program executes opening the puzzle input, and
 * determining the number of steps to get from point AAA to point ZZZ
 * 
 * A sample of the input file:
 * RL
 * AAA = (BBB, CCC)
 * BBB = (DDD, EEE)
 * CCC = (ZZZ, GGG)
 * DDD = (DDD, DDD)
 * EEE = (EEE, EEE)
 * GGG = (GGG, GGG)
 * ZZZ = (ZZZ, ZZZ)
 * 
 * Post Notes:
 * Initially, I see this problem as a potential to use a Tree data structure.
 * After analyzing part II problem, it can be seen as a least common multiplier
 * problem. Thus, utilizing recursion
 */
public class day8 {

  private static final String INPUT_FILE = "./resources/day8_input.txt";
  private static String lr_instructions[];
  private static HashMap<String, List<String>> nodes;

  public static void partOne() {
    // create InstructionNode object
    // put into a hash map for later

    String starting_point = "AAA";
    int steps = 0;
    while (!starting_point.equals("ZZZ")) {
      String instruction = lr_instructions[steps % lr_instructions.length];

      starting_point = takeStep(starting_point, instruction);

      steps++;
    }
    System.out.println(steps);
  }

  /**
   * Initially couldve done it by iterating until each starting
   * point ends up at Z, but the process took too long.
   * 
   */
  public static void partTwo() {
    final ArrayList<String> s_nodes = new ArrayList<>();
    nodes.forEach((key, value) -> {
      Pattern p = Pattern.compile("[A]$");
      Matcher matcher = p.matcher(key);
      if (matcher.find()) {
        s_nodes.add(key);
      }
    });

    final ArrayList<String> e_nodes = new ArrayList<>();
    s_nodes.forEach(n -> {
      e_nodes.add(n.replaceAll("[A]$", "Z"));
    });

    int[] distance_to_end = new int[s_nodes.size()];
    for (int i = 0; i < distance_to_end.length; i++) {
      String node = s_nodes.get(i);
      distance_to_end[i] = calculateDistance(node);
    }

    // find greatest common divisor
    // find least common multiplier
    long lcm = findLCM(distance_to_end, 0);
    System.out.println(lcm);
  }

  public static int calculateDistance(String node) {
    int count = 0;

    while (node.charAt(2) != 'Z') {
      String instruction = lr_instructions[count % lr_instructions.length];
      node = takeStep(node, instruction);
      count++;
    }

    return count;
  }

  static long findLCM(int[] arr, int idx) {
    // lcm(a,b) = (a*b/gcd(a,b))
    if (idx == arr.length - 1) {
      return arr[idx];
    }
    int a = arr[idx];
    long b = findLCM(arr, idx + 1);
    return (a * b / gcd(a, b));
  }

  static long gcd(long a, long b) {
    return b == 0 ? a : gcd(b, a % b);
  }

  public static String takeStep(String node, String instruction) {
    switch (instruction) {
      case "L":
        return nodes.get(node).get(0);

      case "R":
        return nodes.get(node).get(1);

      default:
        System.out.println("Invalid Instruction");
        return null;
    }
  }

  public static void init() {
    List<String> lines = InputFileUtil.open_file(INPUT_FILE);
    // get the left,right instruction
    lr_instructions = lines.get(0).split("");
    nodes = new HashMap<>();
    // get the Node mappings
    for (int i = 2; i < lines.size(); i++) {
      /*
       * Idx of node_label
       * 0 - parent
       * 1 - left
       * 2 - right
       */
      Pattern p = Pattern.compile("(\\w+)\\s*=\\s*\\((\\w+),\\s*(\\w+)\\)");
      Matcher m = p.matcher(lines.get(i));
      if (m.find()) {
        String node_parent = m.group(1).trim();
        List<String> node_label = new ArrayList<>() {
          {
            add(m.group(2).trim());
            add(m.group(3).trim());
          }
        };
        nodes.put(node_parent, node_label);
      }
    }
  }

  public static void main(String[] args) {
    init();
    partOne();
    partTwo();
  }
}
