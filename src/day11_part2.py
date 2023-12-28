from day11_part1 import GalaxyNode, GalaxyEdge
import re

INPUT_FILE = './resources/day11_input.txt'
EXPANSION_MULTIPLIER = 1000000


def _apply_multiplier(coordinates: tuple, row_bound, col_bound) -> tuple:
    """
    Applies scaling and shifting based on row and column boundaries.

    Parameters:
    - coordinates (tuple): The original (row, col) coordinates to be transformed.
    - row_bound: List of row boundaries where expansion occurs.
    - col_bound: List of column boundaries where expansion occurs.

    Returns:
    tuple: Transformed coordinates after scaling and shifting.

    Description:
    Method takes a tuple of coordinates (row, col) and adjusts them according
    to the given row and column boundaries. The row_bound and col_bound parameters
    represent where the rows and columns expand to a certain scale factor.
    - For each row boundary less than the original row, a row_multiplier is calculated.
      The original row is then adjusted by subtracting the row_multiplier and adding
      the expanded portion based on the EXPANSION_MULTIPLIER.
    - Similarly, for each column boundary less than the original column, a col_multiplier
      is calculated. The original column is adjusted similarly.

    This method is useful for adapting coordinates to a dynamically expanding grid.
    """
    row = coordinates[0]
    col = coordinates[1]

    row_multiplier = sum(1 for e in row_bound if e < row) # number of expanding row boundaries crossed
    col_multiplier = sum(1 for e in col_bound if e < col) # number of expanding col boundaries crossed
    
    if (row_multiplier > 0): # if any, scale and shift the y-position of the point
        row = (row - row_multiplier) + (row_multiplier * EXPANSION_MULTIPLIER)

    if (col_multiplier > 0): # if any, scale and shift the x-position of the point
        col = (col - col_multiplier) + (col_multiplier * EXPANSION_MULTIPLIER)

    return (row, col)

def _record_empty_space(data : list) -> list:
    """
    Records the indexes which a row consists of no '#' (galaxy).

    Parameters:
    - data (2D array): puzzle input

    Returns:
    list: recorded indices of which row consists of empty spaces
    """
    idx = 0
    empty_idx = []
    for d in data:  # find the indexes of where no galaxies are present
        r = ''.join([str(c) for c in d])
        if (not re.search(r'#', r)):
            empty_idx.append(idx)
        idx += 1

    return empty_idx

def open_file():
    with open(INPUT_FILE, 'r') as file:
        data = [[*f.strip()] for f in file.readlines()]

        empty_rows = _record_empty_space(data) # find rows with empty space indices
        # transpose the 2D array and find cols with empty space indicies
        empty_cols = _record_empty_space(list(map(list, zip(*data))))

        galaxies = []
        galaxy_num = 1

        # build galaxy nodes and calculate their new positions if required
        for r in range(len(data)):
            for c in range(len(data[r])):
                if (data[r][c] == '#'):
                    pos = _apply_multiplier((r, c), empty_rows, empty_cols)
                    galaxies.append(GalaxyNode(galaxy_num, pos))
                    galaxy_num += 1


        # link nodes together
        for i in range(len(galaxies)):
            curr_galaxy = galaxies[i]
            for g in galaxies[i:]:
                curr_galaxy.connectGalaxies(g)

        return galaxies


if __name__ == '__main__':
    galaxies = open_file()  # open file and gather where empty rows and empty cols exists
    sum_of_shortest = 0
    for g in galaxies:
        sum_of_shortest += g.sumPaths()
    print(f"Sum of the puzzle input length {sum_of_shortest}")