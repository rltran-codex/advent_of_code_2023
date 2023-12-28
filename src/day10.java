import java.util.List;
import java.util.Stack;

import util.InputFileUtil;
import util.PipeGraph;

/**
 * day10 contains the solutions to both part 1 and 2. 
 * The biggest challenge was to create nodes and implement the correct logic to connect each node
 * together. Once that obstacle was overcomed, the problems were nicely set up to be solved.
 * 
 * Refer to PipeGraph.java in the util
 */
public class day10 {
  private static final String INPUT_FILE = "./resources/day10_input.txt";
  private static PipeGraph pnHandler;
  private static int[] starting_point;

  public static void partOne() {
    int size = pnHandler.findLongestDisanceFromAnimal(starting_point);
    System.out.println("Longest distance from animal: " + size);
  }

  public static void partTwo() {
    int numOfEnclosed = pnHandler.findNests(starting_point);
    System.out.println("Number of enclosed tiles: " + numOfEnclosed);
  }

  /**
   * Initializes the PipeGraph 2D board
   * and generates nodes and connects them accordingly
   * based on their neighbors.
   */
  public static void init() {
    // open file
    List<String> lines = InputFileUtil.open_file(INPUT_FILE);

    // create PipeGraph object
    int rows = lines.size();
    int cols = lines.get(0).length();
    pnHandler = new PipeGraph(rows, cols);

    // 2D array of puzzle input
    String[][] tiles = new String[rows][cols];
    starting_point = new int[2];

    // build the 2D array
    for (int r = 0; r < tiles.length; r++) {
      String[] tile = lines.get(r).split("");
      for (int c = 0; c < tiles[r].length; c++) {
        if (tile[c].equals("S")) { // if current tile is S, then save starting point coordinates
          starting_point[0] = r;
          starting_point[1] = c;
        }
        tiles[r][c] = tile[c];
      }
    }

    pnHandler.addPipeNode(starting_point, "S"); // animal starting point
    Stack<Integer[]> nodes = new Stack<>();
    nodes.add(new Integer[] { starting_point[0], starting_point[1] });
    do {
      Integer[] tile = nodes.pop();
      Stack<Integer[]> valid_connections = checkNeighbors(tile, tiles);

      Stack<Integer[]> removeFromStack = new Stack<>();
      for (Integer[] e : valid_connections) {
        int[] coordinates = new int[] { e[0], e[1] };
        String label = tiles[coordinates[0]][coordinates[1]];

        // if adding pipenode returns null, then the pipe has already been added
        if (pnHandler.addPipeNode(coordinates, label) == null) {
          removeFromStack.add(e);
        }

        int[] src_node = new int[] { tile[0], tile[1] };
        pnHandler.connectPipes(src_node, coordinates);
      }

      valid_connections.removeAll(removeFromStack);
      nodes.addAll(valid_connections);
    } while (!nodes.empty());
  }

  public static String getTile(String[][] tiles, int row, int col) {
    try {
      String pipe = tiles[row][col];
      return pipe.equals(".") ? null : pipe;
    } catch (IndexOutOfBoundsException e) {
      return null;
    }
  }

  /**
   * Method checks the neighbors of the current tile's position in a 2D array.
   * Utilizes the method validateTileConnection and adds to stack if the
   * current tile has valid neighboring nodes.
   * 
   * @param curr_tile - current tile to evaluate
   * @param tiles     - 2D array of input map
   * @return nodes_to_connect - valid nodes if any
   */
  public static Stack<Integer[]> checkNeighbors(Integer[] curr_tile, String[][] tiles) {
    int row = curr_tile[0];
    int col = curr_tile[1];
    String pipe = tiles[row][col];
    String above = getTile(tiles, row - 1, col);
    String below = getTile(tiles, row + 1, col);
    String left = getTile(tiles, row, col - 1);
    String right = getTile(tiles, row, col + 1);

    Stack<Integer[]> nodes_to_connect = new Stack<>();
    switch (pipe) {
      case "S": // if animal, check all sides to see if there are any valid connection points
        if (validateTileConnection(Position.UP, above)) {
          nodes_to_connect.add(new Integer[] { row - 1, col });
        }
        if (validateTileConnection(Position.DOWN, below)) {
          nodes_to_connect.add(new Integer[] { row + 1, col });
        }
        if (validateTileConnection(Position.RIGHT, right)) {
          nodes_to_connect.add(new Integer[] { row, col + 1 });
        }
        if (validateTileConnection(Position.LEFT, left)) {
          nodes_to_connect.add(new Integer[] { row, col - 1 });
        }
        break;

      case "|": // Vertical pipe, check only UP and DOWN
        if (validateTileConnection(Position.UP, above)) {
          nodes_to_connect.add(new Integer[] { row - 1, col });
        }
        if (validateTileConnection(Position.DOWN, below)) {
          nodes_to_connect.add(new Integer[] { row + 1, col });
        }

        break;
      case "-": // Horizontal Pipe, check only LEFT and RIGHT
        if (validateTileConnection(Position.RIGHT, right)) {
          nodes_to_connect.add(new Integer[] { row, col + 1 });
        }
        if (validateTileConnection(Position.LEFT, left)) {
          nodes_to_connect.add(new Integer[] { row, col - 1 });
        }
        break;

      case "L": // 90-degree bend connecting north and east, check UP and RIGHT
        if (validateTileConnection(Position.UP, above)) {
          nodes_to_connect.add(new Integer[] { row - 1, col });
        }
        if (validateTileConnection(Position.RIGHT, right)) {
          nodes_to_connect.add(new Integer[] { row, col + 1 });
        }
        break;

      case "J": // 90-degree bend connecting north and west, check UP and LEFT
        if (validateTileConnection(Position.UP, above)) {
          nodes_to_connect.add(new Integer[] { row - 1, col });
        }
        if (validateTileConnection(Position.LEFT, left)) {
          nodes_to_connect.add(new Integer[] { row, col - 1 });
        }
        break;

      case "7": // 90-degree bend connecting south and west, check DOWN and LEFT
        if (validateTileConnection(Position.DOWN, below)) {
          nodes_to_connect.add(new Integer[] { row + 1, col });
        }
        if (validateTileConnection(Position.LEFT, left)) {
          nodes_to_connect.add(new Integer[] { row, col - 1 });
        }
        break;

      case "F": // 90-degree bend connecting south and east, check DOWN and RIGHT
        if (validateTileConnection(Position.DOWN, below)) {
          nodes_to_connect.add(new Integer[] { row + 1, col });
        }
        if (validateTileConnection(Position.RIGHT, right)) {
          nodes_to_connect.add(new Integer[] { row, col + 1 });
        }
        break;

      default:
        break;
    }

    return nodes_to_connect;
  }

  /**
   * Method validates whether the tile above, below, right, or left contain
   * the correct pipe type.
   * - UP is valid if |, F, or 7
   * - DOWN is valid if |, L, or J
   * - LEFT is valid if -, L, or F
   * - RIGHT is valid if -, 7, or J
   * 
   * @param pos        - Position enum for the switch case
   * @param tile_label - the label of the tile to evaluate
   * 
   * @return boolean, true if valid connection
   */
  public static boolean validateTileConnection(Position pos, String tile_label) {
    boolean valid = false;
    if (tile_label == null) {
      return false;
    }
    switch (pos) {
      case UP:
        if (tile_label.equals("|") || tile_label.equals("F") || tile_label.equals("7")) {
          valid = true;
        }
        break;

      case DOWN:
        if (tile_label.equals("|") || tile_label.equals("L") || tile_label.equals("J")) {
          valid = true;
        }
        break;

      case LEFT:
        if (tile_label.equals("-") || tile_label.equals("L") || tile_label.equals("F")) {
          valid = true;
        }
        break;

      case RIGHT:
        if (tile_label.equals("-") || tile_label.equals("7") || tile_label.equals("J")) {
          valid = true;
        }
        break;

      default:
        break;
    }

    return valid;
  }

  public static void main(String[] args) {
    init();
    partOne();
    partTwo();
  }

  /**
   * Enum class to check the tile UP, DOWN, LEFT, or RIGHT
   */
  private enum Position {
    UP,
    DOWN,
    LEFT,
    RIGHT
  }
}
