import * as fs from "fs";
let nodes: Node[][] = [];
let rows: number = undefined;
let cols: number = undefined;
/**
 * Open puzzle input and process it into a Graph data structure.
 *
 * @returns nodeLayout - Graph data structure of all location points.
 */
function buildNodes(): Node[][] {
  const lines = fs.readFileSync("./resources/sample_input/day17.txt", "utf-8");
  // const lines = fs.readFileSync("./resources/day17_input.txt", "utf-8");
  const data: string[][] = lines.split("\r\n").map((line) => line.split(""));
  rows = data.length;
  cols = data[0].length;

  const nodeLayout: Node[][] = Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => null)
  );

  // load nodes
  data.flat().forEach((value, i) => {
    const row = Math.floor(i / cols);
    const col = i % cols;

    const loc = [row, col];
    const nNode = new Node(+value, loc);

    nodeLayout[row][col] = nNode;
  });

  // connect nodes
  nodeLayout.flat().forEach((value, i) => {
    const row = Math.floor(i / cols);
    const col = i % cols;
    let up: Node,
      down: Node,
      left: Node,
      right: Node = undefined;
    if (row > 0) {
      up = nodeLayout[row - 1][col]; // connect up node
    }

    if (row < rows - 1) {
      down = nodeLayout[row + 1][col]; // connect down node
    }

    if (col > 0) {
      left = nodeLayout[row][col - 1]; // connect left node
    }

    if (col < cols - 1) {
      right = nodeLayout[row][col + 1]; // connect right node
    }

    nodeLayout[row][col].setNeighbors([up, down, left, right]);
  });

  return nodeLayout;
}

/**
 * Could use Dijkstra's shortest path algorithm.
 * Keep in mind that the crucible has moving conditions:
 * - Direction movement cannot exceed 3
 * - Must make a right to reset movement counter
 * - Cannot revisit a tile (node)
 * - Goal is to move with the least amount of heat loss
 */

/**
 * Graph Data Structure
 */
interface NodeInterface {
  val: number;
  adj: NodeInterface[];
  loc: number[];

  getAdjList(): NodeInterface[];
}

class Node implements NodeInterface {
  val: number;
  adj: NodeInterface[];
  loc: number[];

  constructor(val: number, loc: number[]) {
    this.val = val;
    this.loc = loc;
    this.adj = [];
  }

  getAdjList = (): NodeInterface[] => {
    return this.adj;
  };

  setNeighbors = (adjList: NodeInterface[]): undefined => {
    if (adjList.length === 0) {
      return;
    }

    // filter out any undefined elements from the list
    this.adj = adjList.filter((node) => node !== undefined);
  };
}

/**
 * Dijsktra's algorithm to find the path
 * that generates the least amount of heat
 * loss to the cruicble.
 *
 * @param s - crucible starting point.
 *
 * references:
 * https://www.digitalocean.com/community/tutorials/min-heap-binary-tree
 * https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
 */
function dijkstraAlgo(srcNode: NodeInterface, destNode: NodeInterface) {
  type NodeInfo = {
    heatLost: number;
    node: NodeInterface;
    prevNode : NodeInterface;
  };

  const dijkstraPath : NodeInterface[][] = Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => null)
  ); // path to take
  
  const queue: NodeInfo[] = []; // "priority queue" (change to minheap for greater performance)
  const heatLossMap = new Map<NodeInterface, number>(); // data object to store heat loss
  const visited = new Set<NodeInterface>(); // visited nodes

  nodes.flat().forEach((value) => {
    /**
     * set source node's heat loss value to 0 and
     * set all other nodes' heat loss values to "infinity"
     */
    heatLossMap.set(value, value === srcNode ? 0 : Number.POSITIVE_INFINITY);
    const [row, col] = value.loc;
    dijkstraPath[row][col] = new Node(value.val, [row, col]); // create empty node with just val and location
  });
  
  queue.push({ heatLost: 0, node: srcNode , prevNode: null});

  while (queue.length !== 0) {
    // pop first node in queue
    const { node: currNode, heatLost: h, prevNode: prevNode } = queue.shift();
    if (visited.has(currNode)) {
      continue;
    }

    visited.add(currNode); // mark node as visited
    // for each adjacent node that hasn't been visited, calculate heat loss of adjacent nodes
    currNode.getAdjList().forEach((e: NodeInterface) => {
      if (!visited.has(e)) {
        const calculateHeatLoss: number = heatLossMap.get(currNode) + e.val;
        let currHeatLoss: number = heatLossMap.get(e);
        
        if (calculateHeatLoss < currHeatLoss) {
          heatLossMap.set(e, calculateHeatLoss);
          queue.push({ heatLost: calculateHeatLoss, node: e , prevNode: currNode});
        }
      }
    });
    queue.sort((a, b) => a.heatLost - b.heatLost); // queue the adj node with the smallest heat loss
    
    const [row, col] = currNode.loc;
    const nNode = dijkstraPath[row][col];
    if (prevNode !== null) {
      const pNode = dijkstraPath[prevNode.loc[0]][prevNode.loc[1]];

      // connect nodes with edge
      nNode.adj.push(pNode);
      pNode.adj.push(nNode);
    }
  }

  console.log("hi");
}

function partOne() {
  let start: number,
    end: number = undefined;
  start = performance.now();
  nodes = buildNodes();
  end = performance.now();
  console.log(`Time to build graph: ${end - start} ms`);
  start = performance.now();
  dijkstraAlgo(nodes[0][0], nodes[rows - 1][cols - 1]);
  end = performance.now();
  console.log(`Time to execute Dijkstra's Shortest Path: ${end - start} ms`);
}

partOne();
