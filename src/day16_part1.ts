import * as fs from "fs";

const lines = fs.readFileSync("./resources/day16_input.txt", "utf-8");
// const lines = fs.readFileSync("./resources/sample_input/day16.txt", "utf-8");
const data: string[][] = lines.split("\r\n").map((line) => Array.from(line));

enum beam_direction {
  UP,
  DOWN,
  RIGHT,
  LEFT,
}

function energizePlatform(data: string[][]) {
  const rows = data.length;
  const cols = data[0].length;

  let e_platform: string[][] = Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => ".")
  );
  let stepStack = new Array();

  // deploy beam and evaluate the number of energized tiles
  stepStack.push([beam_direction.RIGHT, [0, 0]]);
  while (stepStack.length != 0) {
    let curr_loc = stepStack.pop();
    let curr_dir = curr_loc.shift();
    let row = curr_loc[0][0];
    let col = curr_loc[0][1];
    curr_loc = curr_loc[0];

    // validate the row and col
    if (row < 0 || row > rows - 1 || col < 0 || col > cols - 1) {
      continue;
    }

    const eval_pos = data[row][col];
    if (eval_pos === ".") {
      stepStack.push([curr_dir, direction_handler(curr_dir, curr_loc)]);
    } else if (eval_pos === "\\") {
      handleBackSlash(curr_dir, stepStack, curr_loc);
    } else if (eval_pos === "/") {
      handleForwardSlash(curr_dir, stepStack, curr_loc);
    } else if (eval_pos === "|" && e_platform[row][col] !== "#") {
      handleVerticalSplit(curr_dir, stepStack, curr_loc);
    } else if (eval_pos === "-" && e_platform[row][col] !== "#") {
      handleHorizontalSplit(curr_dir, stepStack, curr_loc);
    }

    e_platform[row][col] = "#";
  }

  console.log(
    "Total number of energized tiles: " +
      e_platform.flat().filter((i) => i === "#").length
  );
}

function handleVerticalSplit(
  dir: beam_direction,
  stack: any[],
  coordinates: number[]
) {
  if (
    dir === (beam_direction.DOWN as beam_direction) ||
    dir === (beam_direction.UP as beam_direction)
  ) {
    stack.push([dir, direction_handler(dir, coordinates)]);
    return;
  }

  // add the left
  stack.push([
    beam_direction.DOWN,
    direction_handler(beam_direction.DOWN, coordinates),
  ]);
  // add the right
  stack.push([
    beam_direction.UP,
    direction_handler(beam_direction.UP, coordinates),
  ]);
}

function handleHorizontalSplit(
  dir: beam_direction,
  stack: any[],
  coordinates: number[]
) {
  if (
    dir === (beam_direction.RIGHT as beam_direction) ||
    dir === (beam_direction.LEFT as beam_direction)
  ) {
    stack.push([dir, direction_handler(dir, coordinates)]);
    return;
  }

  // add the left
  stack.push([
    beam_direction.LEFT,
    direction_handler(beam_direction.LEFT, coordinates),
  ]);
  // add the right
  stack.push([
    beam_direction.RIGHT,
    direction_handler(beam_direction.RIGHT, coordinates),
  ]);
}

function handleBackSlash(
  dir: beam_direction,
  stack: any[],
  coordinates: number[]
) {
  switch (
    dir // "\"
  ) {
    case beam_direction.UP as beam_direction:
      stack.push([beam_direction.LEFT, [coordinates[0], coordinates[1] - 1]]);
      break;
    case beam_direction.DOWN as beam_direction:
      stack.push([beam_direction.RIGHT, [coordinates[0], coordinates[1] + 1]]);
      break;
    case beam_direction.RIGHT as beam_direction:
      stack.push([beam_direction.DOWN, [coordinates[0] + 1, coordinates[1]]]);
      break;
    case beam_direction.LEFT as beam_direction:
      stack.push([beam_direction.UP, [coordinates[0] - 1, coordinates[1]]]);
      break;

    default:
      break;
  }
}

function handleForwardSlash(
  dir: beam_direction,
  stack: any[],
  coordinates: number[]
) {
  switch (
    dir // "/"
  ) {
    case beam_direction.UP as beam_direction:
      stack.push([beam_direction.RIGHT, [coordinates[0], coordinates[1] + 1]]);
      break;
    case beam_direction.DOWN as beam_direction:
      stack.push([beam_direction.LEFT, [coordinates[0], coordinates[1] - 1]]);
      break;
    case beam_direction.RIGHT as beam_direction:
      stack.push([beam_direction.UP, [coordinates[0] - 1, coordinates[1]]]);
      break;
    case beam_direction.LEFT as beam_direction:
      stack.push([beam_direction.DOWN, [coordinates[0] + 1, coordinates[1]]]);
      break;

    default:
      break;
  }
}

function direction_handler(direction: beam_direction, coordinates: number[]) {
  let row: number;
  let col: number;

  switch (direction) {
    case beam_direction.UP:
      row = coordinates[0] - 1;
      col = coordinates[1];
      break;
    case beam_direction.DOWN:
      row = coordinates[0] + 1;
      col = coordinates[1];
      break;
    case beam_direction.RIGHT:
      row = coordinates[0];
      col = coordinates[1] + 1;
      break;
    case beam_direction.LEFT:
      row = coordinates[0];
      col = coordinates[1] - 1;
      break;
  }

  return [row, col];
}

const start = performance.now();
energizePlatform(data);
const end = performance.now();
console.log(`Time: ${(end - start)} ms`);