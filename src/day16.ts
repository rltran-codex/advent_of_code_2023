import * as fs from "fs";

const lines = fs.readFileSync("./resources/day16_input.txt", "utf-8");
// const lines = fs.readFileSync("./resources/sample_input/day16.txt", "utf-8");
const data: string[][] = lines.split("\r\n").map((line) => Array.from(line));

enum BeamDirection {
  UP,
  DOWN,
  RIGHT,
  LEFT,
}

interface BeamCoordinate {
  row:number;
  col:number;
  dir:BeamDirection;
}

function energizePlatform(data: string[][], stepStack : any[]) {
  const rows = data.length;
  const cols = data[0].length;

  let e_platform: string[][] = Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => ".")
  );
  // deploy beam and evaluate the number of energized tiles
  while (stepStack.length != 0) {
    let { dir, row, col } = stepStack.pop() as BeamCoordinate;
    let curr_loc = [row, col];

    // validate the row and col
    if (row < 0 || row > rows - 1 || col < 0 || col > cols - 1) {
      continue;
    }

    const eval_pos = data[row][col];
    if (eval_pos === ".") {
      let [row, col] = direction_handler(dir, curr_loc);
      stepStack.push({dir:dir, row:row, col:col});
    } else if (eval_pos === "\\") {
      handleBackSlash(dir, stepStack, curr_loc);
    } else if (eval_pos === "/") {
      handleForwardSlash(dir, stepStack, curr_loc);
    } else if (eval_pos === "|" && e_platform[row][col] !== "#") {
      handleVerticalSplit(dir, stepStack, curr_loc);
    } else if (eval_pos === "-" && e_platform[row][col] !== "#") {
      handleHorizontalSplit(dir, stepStack, curr_loc);
    }

    e_platform[row][col] = "#";
  }

  let result = e_platform.flat().filter((i) => i === "#").length;
  // console.log(`Total number of energized tiles: ${result}`);
  return result;
}

function handleVerticalSplit(
  dir: BeamDirection,
  stack: any[],
  coordinates: number[]
) {
  if (
    dir === (BeamDirection.DOWN as BeamDirection) ||
    dir === (BeamDirection.UP as BeamDirection)
  ) {
    const [row, col] = direction_handler(dir, coordinates);
    stack.push({dir:dir, row:row, col:col});
    return;
  }

  let [row, col] = direction_handler(BeamDirection.DOWN, coordinates);
  // add the left
  stack.push([
    {
      dir:BeamDirection.DOWN,
      row:row,
      col:col
    }
  ]);
  // add the right
  [row, col] = direction_handler(BeamDirection.UP, coordinates);
  stack.push([
    {
      dir:BeamDirection.UP,
      row:row,
      col:col
    }
  ]);
}

function handleHorizontalSplit(
  dir: BeamDirection,
  stack: any[],
  coordinates: number[]
) {
  if (
    dir === (BeamDirection.LEFT as BeamDirection) ||
    dir === (BeamDirection.RIGHT as BeamDirection)
  ) {
    const [row, col] = direction_handler(dir, coordinates);
    stack.push({dir:dir, row:row, col:col});
    return;
  }

  let [row, col] = direction_handler(BeamDirection.RIGHT, coordinates);
  // add the left
  stack.push([
    {
      dir:BeamDirection.RIGHT,
      row:row,
      col:col
    }
  ]);
  // add the right
  [row, col] = direction_handler(BeamDirection.LEFT, coordinates);
  stack.push([
    {
      dir:BeamDirection.LEFT,
      row:row,
      col:col
    }
  ]);
}

function handleBackSlash(
  dir: BeamDirection,
  stack: any[],
  coordinates: number[]
) {
  switch (
    dir // "\"
  ) {
    case BeamDirection.UP as BeamDirection:
      stack.push({dir: BeamDirection.LEFT, row:coordinates[0], col: coordinates[1] - 1});
      break;
    case BeamDirection.DOWN as BeamDirection:
      stack.push({dir: BeamDirection.RIGHT, row:coordinates[0], col: coordinates[1] + 1});
      break;
    case BeamDirection.RIGHT as BeamDirection:
      stack.push({dir: BeamDirection.DOWN, row:coordinates[0] + 1, col: coordinates[1]});
      break;
    case BeamDirection.LEFT as BeamDirection:
      stack.push({dir: BeamDirection.UP, row:coordinates[0] - 1, col: coordinates[1]});
      break;

    default:
      break;
  }
}

function handleForwardSlash(
  dir: BeamDirection,
  stack: any[],
  coordinates: number[]
) {
  switch (
    dir // "/"
  ) {
    case BeamDirection.UP as BeamDirection:
      stack.push({dir: BeamDirection.RIGHT, row: coordinates[0], col: coordinates[1] + 1});
      break;
    case BeamDirection.DOWN as BeamDirection:
      stack.push({dir: BeamDirection.LEFT, row: coordinates[0], col: coordinates[1] - 1});
      break;
    case BeamDirection.RIGHT as BeamDirection:
      stack.push({dir: BeamDirection.UP, row: coordinates[0] - 1, col: coordinates[1]});
      break;
    case BeamDirection.LEFT as BeamDirection:
      stack.push({dir: BeamDirection.DOWN, row: coordinates[0] + 1, col: coordinates[1]});
      break;

    default:
      break;
  }
}

function direction_handler(direction: BeamDirection, coordinates: number[]) {
  let row: number;
  let col: number;

  switch (direction) {
    case BeamDirection.UP:
      row = coordinates[0] - 1;
      col = coordinates[1];
      break;
    case BeamDirection.DOWN:
      row = coordinates[0] + 1;
      col = coordinates[1];
      break;
    case BeamDirection.RIGHT:
      row = coordinates[0];
      col = coordinates[1] + 1;
      break;
    case BeamDirection.LEFT:
      row = coordinates[0];
      col = coordinates[1] - 1;
      break;
  }

  return [row, col];
}

function findMaxEnergy(data : string[][]) {
  type Coordinates = [number, number];
  let edge_points = new Array();
  const rows = data.length;
  const cols = data[0].length;

  // upper left
  edge_points.push({dir:BeamDirection.RIGHT, row:0, col:0});
  edge_points.push({dir: BeamDirection.DOWN, row:0, col:0});
  
  // upper right
  edge_points.push({dir: BeamDirection.LEFT, row:0, col:cols - 1});
  edge_points.push({dir: BeamDirection.DOWN, row:0, col:cols - 1});

  // lower left
  edge_points.push({dir: BeamDirection.UP, row:rows - 1, col:0});
  edge_points.push({dir: BeamDirection.RIGHT, row:rows - 1, col:0});

  // lower right
  edge_points.push({dir: BeamDirection.UP, row:rows - 1, col: cols - 1});
  edge_points.push({dir: BeamDirection.LEFT, row:rows - 1, col: cols - 1});

  // upper and lower most edges
  for (let col = 1; col < cols - 1; col++) {
    edge_points.push({dir: BeamDirection.DOWN, row:0, col: col});
    edge_points.push({dir: BeamDirection.UP, row:rows - 1, col: col});
  }

  // right and left most edges
  for (let row = 1; row < rows - 1; row++) {
    edge_points.push({dir: BeamDirection.RIGHT, row:row, col: 0});
    edge_points.push({dir: BeamDirection.LEFT, row:row, col: cols - 1});
  }

  var max = Number.MIN_SAFE_INTEGER;
  edge_points.forEach((value) => {
    let stepStack = new Array();
    stepStack.push(value);
    let r = energizePlatform(data, stepStack)
    if (r > max) {
      max = r;
    }
  });

  return max;
}

let start = performance.now();
let stepStack = new Array();
stepStack.push({dir:BeamDirection.RIGHT, row:0, col:0});
const result_1 = energizePlatform(data, stepStack);
let end = performance.now();
console.log(`Part 1, energized tiles: ${result_1}`);
console.log(`Time: ${(end - start)} ms`);

// for part two, its a little more time consuming
// the idea is to mark all the starting points and their direction
// and feed it to energizePlatform() method to calculate the number
// of energized tiles

start = performance.now();
let result_2 = findMaxEnergy(data);
end = performance.now();
console.log(`Part 2, energized tiles: ${result_2}`);
console.log(`Time: ${(end - start)} ms`);