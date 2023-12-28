"""
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. 
However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. 
In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.
"""
import re
import sys

INPUT_FILE = './resources/day11_input.txt'


        
class GalaxyNode:
  def __init__(self, galaxy_num : int, pos : tuple):
      self.galaxy_num = galaxy_num
      self.pos = pos
      self.edges = {}

  def connectGalaxies(self, dest):
      if dest == self:
          return
      self.edges[dest.galaxy_num] = GalaxyEdge(self, dest)

  def sumPaths(self):
      sum = 0
      for edge in self.edges.values():
          sum += edge.length
      
      return sum

  
  def shortest_path(self):
      shortest_path = sys.maxsize
      if len(self.edges) == 0:
          return 0
      for galaxy, edge in self.edges.items():
          if edge.length < shortest_path:
              shortest_path = edge.length

      return shortest_path

class GalaxyEdge:
    def __init__(self, src : GalaxyNode, dest : GalaxyNode):
        self.src = src
        self.dest = dest
        self.length = self._calculate_distance()

    def _calculate_distance(self) -> int:
        x1 = self.src.pos[0]
        x2 = self.dest.pos[0]
        y1 = self.src.pos[1]
        y2 = self.dest.pos[1]
        return abs(x2 - x1) + abs(y2 - y1)


def domain_expansion(data: list) -> list:
    new_data = []
    for d in data:  # find the indexes of where no galaxies are present
        r = ''.join([str(c) for c in d])
        if (not re.search(r'#', r)):
            new_data.append(d)
        new_data.append(d)

    return new_data

def open_file():
    galaxies = []
    data = []
    
    with open(INPUT_FILE, 'r') as file:
        # read file and store data in 2D array
        data = [[*f.strip()] for f in file.readlines()]

        # expand rows that contain no galaxies
        data = domain_expansion(data)

        # transpose 2D array to process expanding columns
        l2 = list(map(list, zip(*data)))
        l2 = domain_expansion(l2)

        # transpose data again to reset orientation
        data = list(map(list, zip(*l2)))
        # replace # with number
        galaxy_num = 1
        for i in range(len(data)):
          for j in range(len(data[i])):
              if (data[i][j] == '#'):
                  galaxies.append(GalaxyNode(galaxy_num, (i, j)))
                  galaxy_num += 1

    # connect galaxies
    for i in range(len(galaxies)):
        curr_galaxy = galaxies[i]
        for g in galaxies[i:]:
          curr_galaxy.connectGalaxies(g)
    return galaxies

if __name__ == "__main__":
  galaxies = open_file()

  sum_of_shortest = 0
  for g in galaxies:
      sum_of_shortest += g.sumPaths()

  print(f"Sum of the puzzle input length {sum_of_shortest}")