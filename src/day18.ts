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
      point = dirHandler(dir, point, 1);
      lpoints.push({ point: point, color: color });
    }
  }

  // using shoelace and  pick's theorem to find the area of the polygon
  return calculateInteriorPoints(lpoints, lpoints.length) + lpoints.length;
}


function hexDig(encodedInstrs: digInstruction[]): number {
  function decodeDir(dir:number) {
    switch (dir) {
      case 0:
        return 'R';
      case 1:
        return 'D';
      case 2:
        return 'L';
      case 3:
        return 'U';
    }
  }
  
  // decode new dig instructions
  const decodedInstrs = [];
  encodedInstrs.forEach((v) => {
    let [n_steps, dir] = hexExtract(v.color);
    let n_dir = decodeDir(dir);
    decodedInstrs.push({dir:n_dir, n_steps:n_steps});
  });

  let point = [0, 0];
  let lpoints = [];
  let total = 0;

  // these are too large of values, so only use the beginning, middle,  and end of lattice points
  while (decodedInstrs.length > 0) {
    const {dir, n_steps} = decodedInstrs.shift();
    // take only the beginning point, middle point, and the ending point; mimic creating a 'line' between the two points
    const s_point = dirHandler(dir, point, 1);
    const m_point = dirHandler(dir, point, Math.floor(n_steps / 2));
    const e_point = dirHandler(dir, point, n_steps);

    point = e_point; // update 'pencil point'

    lpoints.push({point:s_point});
    lpoints.push({point:m_point});
    lpoints.push({point:e_point});

    total += n_steps;
  }


  return calculateInteriorPoints(lpoints, total) + total;
}

function hexExtract(hex: string) {
  const n_steps: string = hex.substring(0, 5);
  const dir: string = hex.substring(5);

  return [parseInt(n_steps, 16), parseInt(dir, 16)];
}

function dirHandler(dir: string, coordinate: number[], n_steps: number) {
  switch (dir) {
    case "U":
      return [coordinate[0] - n_steps, coordinate[1]];
    case "D":
      return [coordinate[0] + n_steps, coordinate[1]];
    case "L":
      return [coordinate[0], coordinate[1] - n_steps];
    case "R":
      return [coordinate[0], coordinate[1] + n_steps];
  }
}

/**
 * Uses shoelace formula and Pick's theorem to determine
 * the number of interior points in the polygon.
 * 
 * @param points array of boundary lattice points
 * @returns 
 */
function calculateInteriorPoints(points: digPoint[], boundaryPoints: number) {
  const numPoints = points.length;
  let area = 0;

  for (let i = 0; i < numPoints - 1; i++) {
    const { point: n1 } = points[i];
    const { point: n2 } = points[(i + 1) % numPoints];

    area += (n2[0] + n1[0]) * (n2[1] - n1[1]);
  }

  area = Math.abs(area) / 2;

  return area - (boundaryPoints / 2) + 1;
}


// part 1
let start = performance.now();
console.log(`part 1: ${dig(readFile("./resources/day18_input.txt"))}`);
let end = performance.now();
console.log(`Time: ${(end - start)} ms`);

start = performance.now();
console.log(`part 2: ${hexDig(readFile("./resources/day18_input.txt"))}`);
end = performance.now();
console.log(`Time: ${(end - start)} ms`);