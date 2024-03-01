import * as fs from "fs";
import { PriorityQueue } from "./util/PriorityQueue";

/**
 * Notes for me:
 * A potential way to do this is to use dijkstra's algorithm to traverse the shortest path.
 * However, the issue with this is that the crucible can move in one direction without having the restrictions.
 * If we add a way to keep track of which direction the crucible is heading, and if we reach the limit of 3 steps in a
 * single direction, we can recalculate the dijkstra's path for each direction to find the optimized movement.
 *
 * One theory we can use is that the algorithm will calculate the minimum distance heat from the source to the destination.
 * So if we traverse the first iteration of calculation then the crucible is forced to change direction,  we can change the
 * direction and recalculate the least amount of heat loss.
 *
 * Another theory is that we can have a counter that checks the current direction number, if stepDirection < 3, there are potentially
 * numberofAdj - 1 (visited node). If stepDirection == 3, then there are potentially only numberOfAdj - 1 (visited node) - 1 (curr direction)
 */

let nodeList: Node[][] = []; // list of all nodes in graph
let rows: number;
let cols: number;

function partOne() {
  nodeList = buildNodes();
  dijkstraAlgo(nodeList[0][0], nodeList[rows - 1][cols - 1]);
}

function dijkstraAlgo(srcNode: Node, destNode: Node) {
  function drawMap(dir: Direction) {
    switch (dir) {
      case Direction.UP:
        return "^"
      case Direction.DOWN:
        return "v"
      case Direction.LEFT:
        return "<"
      case Direction.RIGHT:
        return ">"    
      default:
        break;
    }
  }
  const pq: PriorityQueue<NodeInfo> = new PriorityQueue<NodeInfo>(
    (a: NodeInfo, b: NodeInfo) => {
      return a.minHL > b.minHL;
    }
  );

  const crucibleMap: string[][] = Array.from({ length: rows }, () => Array.from({ length: cols }, () => undefined));

  const heatLossMap = new Map<Node, number>();
  nodeList.flat().forEach((v) => {
    v.visited = false; // set all nodes to unvisited
    // set all nodes that are not srcNode to infinity
    heatLossMap.set(v, v === srcNode ? 0 : Number.POSITIVE_INFINITY);
  });

  pq.push({ node: srcNode, minHL: 0, dir: undefined, stepCnt: 0 });

  while (!pq.isEmpty()) {
    const {
      // pop the MinHeap queue
      node: currNode,
      dir: currDir,
      stepCnt: s,
    }: NodeInfo = pq.pop();

    if (currNode.visited) {
      continue;
    }

    crucibleMap[currNode.location[0]][currNode.location[1]] = drawMap(currDir);
    currNode.visited = true;
    for (const [dir, adjNode] of Array.from(currNode.adjList.entries())) {
      if (!adjNode.visited) {
        if (dir === currDir && s === 3) {
          continue;
        }
  
        const calcHL: number = heatLossMap.get(currNode) + adjNode.heatValue; // calculate tentative heat loss
        // if new tentative heat loss is less than current value, update and queue
        if (calcHL < heatLossMap.get(adjNode)) {
          heatLossMap.set(adjNode, calcHL);
          pq.push({
            node: adjNode,
            minHL: calcHL,
            dir: dir,
            stepCnt: dir === currDir || currDir === undefined ? s + 1 : 1,
          });
        }
      }
    }

    console.log('');
  }

  console.log(heatLossMap.get(destNode));
}

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

    nodeLayout[row][col].setAdjList(
      new Map<Direction, Node>([
        [Direction.UP, up],
        [Direction.DOWN, down],
        [Direction.LEFT, left],
        [Direction.RIGHT, right],
      ])
    );
  });

  return nodeLayout;
}

/*
 * Graph Data Structure
 */
/**
 * Direction enum
 *  - UP    [row - 1, col]
 *  - DOWN  [row + 1, col]
 *  - LEFT  [row, col - 1]
 *  - RIGHT [row, col + 1]
 */
enum Direction {
  UP,
  DOWN,
  LEFT,
  RIGHT,
}

type NodeInfo = {
  node: Node;
  minHL: number;
  dir: Direction;
  stepCnt: number;
}

class Node {
  adjList: Map<Direction, Node>;
  location: number[];
  heatValue: number;
  visited: boolean;

  constructor(heatValue: number, location: number[]) {
    this.heatValue = heatValue;
    this.location = location;
    this.adjList = new Map<Direction, Node>();
    this.visited = false;
  }

  getAdjList = (): Map<Direction, Node> => {
    if (this.adjList === undefined) {
      throw new Error(`Node adjList at ${this.location} is undefined.`);
    }

    return this.adjList;
  };

  setAdjList = (adjList: Map<Direction, Node>) => {
    adjList.forEach((v, k) => {
      if (v !== undefined) {
        this.adjList.set(k, v);
      }
    });
  };
}

partOne();
