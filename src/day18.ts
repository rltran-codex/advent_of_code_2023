import * as fs from "fs";

type digInstruction = {
  dir: string;
  n_steps: number;
  color: string;
};

type digPoint = {
  point: number[];
  color: string;
};

function readFile(file) {
  const lines = fs.readFileSync(file, "utf-8").split("\n");
  const data: digInstruction[] = [];

  lines.forEach((v) => {
    const val = v.trim().split(" ");
    const color = val[2].replace(/[()#]/g, "");

    data.push({
      dir: val[0],
      n_steps: parseInt(val[1]),
      color: color,
    });
  });

  return data;
}

function dig(dInstrs: digInstruction[]): number {
  // start drawing starting from position [0, 0]
  // for each point, add to list of lattice points
  let point = [0, 0];
  const lpoints: digPoint[] = [];

  while (dInstrs.length > 0) {
    const { dir, n_steps, color } = dInstrs.shift();
    for (let n = 0; n < n_steps; n++) {
      point = dirHandler(dir, point);
      lpoints.push({ point: point, color: color });
    }
  }

  // using shoelace and  pick's theorem to find the area of the polygon
  return calculateInteriorPoints(lpoints) + lpoints.length;
}

function dirHandler(dir: string, coordinate: number[]) {
  switch (dir) {
    case "U":
      return [coordinate[0] - 1, coordinate[1]];
    case "D":
      return [coordinate[0] + 1, coordinate[1]];
    case "L":
      return [coordinate[0], coordinate[1] - 1];
    case "R":
      return [coordinate[0], coordinate[1] + 1];
  }
}

/**
 * Uses shoelace formula and Pick's theorem to determine
 * the number of interior points in the polygon.
 * 
 * @param points array of boundary lattice points
 * @returns 
 */
function calculateInteriorPoints(points: digPoint[]) {
  const numPoints = points.length;
  let area = 0;

  for (let i = 0; i < numPoints - 1; i++) {
    const { point: n1 } = points[i];
    const { point: n2 } = points[(i + 1) % numPoints];

    area += (n2[0] + n1[0]) * (n2[1] - n1[1]);
  }

  area = Math.abs(area) / 2;

  return area - (numPoints / 2) + 1;
}


// part 1
let start = performance.now();
console.log(`part 1: ${dig(readFile("./resources/day18_input.txt"))}`);
let end = performance.now();
console.log(`Time: ${(end - start)} ms`);