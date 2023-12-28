package util;

import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;
import java.util.Stack;

/**
 * PipeGraph uses a Graph datastructure to solve day 10 problem.
 * - Uses a DFS to find the longest distance from the animal.
 * - Uses Pick's Theroem and Shoelace Formula to calculate the number of
 *   enclosed points.
 * 
 * Post notes:
 * Initially, I wanted to go the route of using a flood fill to solve part II,
 * however it was much easier to combine Pick's theroem and shoelace formula to achieve the
 * same results.
 * Maybe in the future, I may return to this problem and implement a flood fill approach to
 * achieve this.
 */
public class PipeGraph {
  public static List<PipeNode> pipes;
  public static PipeNode[][] pipe_locations;

  public PipeGraph(int row, int col) {
    pipes = new ArrayList<>();
    pipe_locations = new PipeNode[row][col];
  }

  /**
   * Using a DFS algorithm to traverse the cyclic path.
   * Return the size of the loop / 2 to find the longest distance from
   * starting point (animal) in both directions
   * 
   * @param coordinates initial starting point of the animal.
   * @return longest distance from animal in either direction.
   */
  public int findLongestDisanceFromAnimal(int[] coordinates) {
    // grab starting node
    PipeNode sNode = pipe_locations[coordinates[0]][coordinates[1]];
    // start cyclic search from sNode
    CyclicUtil cyclicUtil = new CyclicUtil(sNode);
    Stack<PipeNode> loop = cyclicUtil.detectCyclic();
    if (loop == null) {
      throw new NullPointerException("No cyclic path detected from starting point: " + coordinates);
    }
    return loop.size() / 2;
  }

  /**
   * This method is used to solve Part II of day 10.
   * Uses the starting point, grabs the cyclic loop and
   * caluclates the number of tiles enclosed by the loop by 
   * using the Shoelace formula to find the area, then the number
   * of lattice points enclosed with Pick's Theorem.
   * 
   * Reference: 
   * https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem
   * https://artofproblemsolving.com/wiki/index.php/Pick%27s_Theorem
   * 
   * @param coordinates - Starting point
   * @return number of latice points
   * @throws NullPointerException if no cyclic loop was detected with starting point.
   */
  public int findNests(int[] coordinates) {
    // grab starting node
    PipeNode sNode = pipe_locations[coordinates[0]][coordinates[1]];
    if (sNode == null) {
      throw new NullPointerException("Starting point does not exist as a PipeNode object: " + coordinates);
    }
    // check for cyclic paths
    CyclicUtil cyclicUtil = new CyclicUtil(sNode);
    Stack<PipeNode> bound_loop = cyclicUtil.detectCyclic();
    if (bound_loop == null) {
      throw new NullPointerException("No cyclic loop found with starting point: " + coordinates);
    }

    Object[] loop = bound_loop.toArray(); // boundary points listed clockwise

    // Using shoelace formula to calcualte the Area
    // A = 1/2 |sum((xi+1 + xi)(yi+1 - yi))|
    int numOfPipes = loop.length;
    long shoelace_area = 0;

    for (int i = 0; i < numOfPipes - 1; i++) {
      PipeNode n1 = (PipeNode) loop[i];
      PipeNode n2 = (PipeNode) loop[i + 1 % numOfPipes];
      
      shoelace_area += (n2.getPosition()[0] + n1.getPosition()[0]) * (n2.getPosition()[1] - n1.getPosition()[1]);
    }

    shoelace_area = Math.abs(shoelace_area) / 2;

    // Pick's Theorem
    // A = I + B/2 - 1 => I = A - B/2 + 1
    long i = shoelace_area - (numOfPipes / 2) + 1;
    return (int) i;
  }

  /*
   * PipeGraph utilities functions below
   */

  /**
   * Overload method of addPipeNode(Integer[], String)
   * 
   * @param coordinates
   * @param pipe_label
   * @return
   */
  public PipeNode addPipeNode(int[] coordinates, String pipe_label) {
    return this.addPipeNode(new Integer[] { coordinates[0], coordinates[1] }, pipe_label);
  }

  public PipeNode addPipeNode(Integer[] coordinates, String pipe_label) {
    if (retrieveNode(coordinates) != null) {
      return null;
    }

    int row = coordinates[0];
    int col = coordinates[1];

    PipeNode nPipe = new PipeNode(pipe_label, coordinates);
    pipes.add(nPipe);
    pipe_locations[row][col] = nPipe;
    return nPipe;
  }

  /**
   * Method connects two nodes together by checking
   * if the source and destination exists and bridges
   * connection accordingly if nonexistent.
   * 
   * @param origin
   * @param dest
   */
  public void connectPipes(Integer[] origin, Integer[] dest) {
    PipeNode src_node = retrieveNode(origin);
    PipeNode dest_node = retrieveNode(dest);

    if (src_node == null || dest_node == null) {
      throw new NullPointerException("Unable to bridge connection to nodes that don't exists");
    }
    // check if connection already exists in src node
    boolean srcHasConnection = false;
    for (PipeNode adj : src_node.getAdjNodes()) {
      if (Arrays.equals(adj.getPosition(), dest_node.getPosition())) {
        srcHasConnection = true;
      }
    }

    // check if connection exists in dest node
    boolean destHasConnection = false;
    for (PipeNode adj : dest_node.getAdjNodes()) {
      if (Arrays.equals(adj.getPosition(), src_node.getPosition())) {
        destHasConnection = true;
      }
    }

    if (!srcHasConnection) {
      src_node.connectAdjacentNode(dest_node);
    }
    if (!destHasConnection) {
      dest_node.connectAdjacentNode(src_node);
    }
  }

  /**
   * Overloaded method of connectPipes(Integer[], Integer[])
   * 
   * @param origin
   * @param dest
   */
  public void connectPipes(int[] origin, int[] dest) {
    this.connectPipes(new Integer[] { origin[0], origin[1] }, new Integer[] { dest[0], dest[1] });
  }

  /**
   * Retrieves the node at the specified coordinate.
   * Post notes:
   * this improved the run time significantly as it is
   * a O(1) operation as compared to iterating through
   * massive ammounts of nodes recorded.
   * 
   * @param coordinates
   * @return
   */
  public PipeNode retrieveNode(int[] coordinates) {
    return pipe_locations[coordinates[0]][coordinates[1]];
  }

  /**
   * Overloaded method of retrieveNode(int[])
   * 
   * @param coordinates
   * @return
   */
  public PipeNode retrieveNode(Integer[] coordinates) {
    return this.retrieveNode(new int[] { coordinates[0], coordinates[1] });
  }

  /**
   * Inner class utility to detect cyclic paths
   * for starting node.
   */
  private class CyclicUtil {
    private Stack<PipeNode> visited_pipes;
    private Stack<PipeNode> adj_pipes;
    private PipeNode starting_node;

    public CyclicUtil(PipeNode starting_node) {
      this.starting_node = starting_node;
      this.visited_pipes = new Stack<>();
      this.adj_pipes = new Stack<>();
    }

    /**
     * Method uses a do-while loop to detect
     * a cyclic path with the starting node.
     * 
     * @return null if a loop was not found.
     */
    public Stack<PipeNode> detectCyclic() {
      pipes.forEach(p -> p.resetVisit());

      visited_pipes.add(starting_node);
      adj_pipes.addAll(starting_node.visit());
      if (adj_pipes.isEmpty()) {
        return null;
      }

      boolean isCyclic = false;
      do {
        PipeNode curr = adj_pipes.pop();
        if (!curr.isVisited) {
          visited_pipes.add(curr);
        } 

        if (Arrays.equals(curr.getPosition(), starting_node.getPosition())) {
          isCyclic = true;
          break;
        }

        adj_pipes.addAll(curr.visit());
      } while (!adj_pipes.isEmpty());

      if (isCyclic) {
        return this.visited_pipes;
      } else {
        return null;
      }
    }

    /**
     * Method uses a DFS method recursively to detect
     * a cyclic path.
     * 
     * Post note:
     * This method worked for a small dataset, but when
     * using the actual puzzle input, the program encountered
     * a stack overflow error.
     * 
     * @return visited nodes if a cyclic path was found.
     */
    public Stack<PipeNode> detectCyclicRecur() {
      // mark all nodes as unvisited
      pipes.forEach(p -> p.resetVisit());
      boolean isCyclic = dfsTraversal(starting_node, starting_node);
      if (isCyclic) {
        return visited_pipes;
      } else {
        return null;
      }
    }

    private boolean dfsTraversal(PipeNode curr, PipeNode parent) {
      // visit node
      visited_pipes.add(curr);
      // grab all adjacent nodes
      List<PipeNode> adj = curr.visit();
      // iterate through each adjacent node
        // if node p is not visited, recur
        // else if the node p != parent's location
        // return false
      for (PipeNode n : adj) {
        if (!n.isVisited) {
          if (dfsTraversal(n, curr)) {
            return true;
          }
        } else if (!Arrays.equals(n.getPosition(), parent.getPosition())) {
          return true;
        }
      }
      return false;
    }
  }

  /**
   * Inner class PipeNode to resemble Pipe
   * nodes for the puzzle input.
   */
  private class PipeNode {
    private String node_label;
    private List<PipeNode> adj_nodes;
    private Integer[] pos;
    private boolean isVisited;

    public PipeNode(String node_label, Integer[] pos) {
      this(node_label, pos, new ArrayList<>());
    }

    public PipeNode(String node_label, Integer[] pos, List<PipeNode> adj_list) {
      this.node_label = node_label;
      this.pos = pos;
      this.adj_nodes = adj_list;
      this.isVisited = false;
    }

    public void connectAdjacentNode(PipeNode adj_node) {
      this.adj_nodes.add(adj_node);
    }

    public Integer[] getPosition() {
      return this.pos;
    }

    public String getPipeLabel() {
      return this.node_label;
    }

    public List<PipeNode> getAdjNodes() {
      return this.adj_nodes;
    }

    public void resetVisit() {
      this.isVisited = false;
    }

    /**
     * Visit node and returns all adjacent nodes.
     * 
     * @return List of adjacent nodes if not visited already.
     */
    public List<PipeNode> visit() {
      if (this.isVisited) {
        return new ArrayList<>();
      }
      this.isVisited = true;
      return this.adj_nodes;
    }
  }
}
