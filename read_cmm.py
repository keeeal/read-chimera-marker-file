from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path

import numpy as np
from numpy.linalg import norm
from scipy.spatial import Delaunay


def read_cmm(file: Path) -> np.ndarray:
    """Reads CMM file and returns a Numpy array of shape (npoints, 3)."""

    # Read each line and split by whitespace.
    with open(file) as f:
        lines = map(str.split, f.readlines())

    # Include the origin as the first point.
    points = []

    # Read other points.
    for line in lines:

        # Ignore lines that are not markers.
        if line[0] != "<marker":
            continue

        # Split keys and values by equals sign.
        data = dict(i.split("=") for i in line[1:])

        # Get each value from between the quotes and cast as float.
        for key, value in data.items():
            value = value[value.index('"') + 1 :]
            value = value[: value.index('"')]
            data[key] = float(value)

        # Only keep the X, Y, and Z coordinates.
        points.append([data["x"], data["y"], data["z"]])

    # Return as a Numpy array.
    return np.array(points)


def tri_area(p1, p2, p3) -> float:
    """Calculate the area of a triangle. Each point is an array of shape (3,)"""

    a = p2 - p1
    b = p3 - p1

    area = (1 / 2) * norm(np.cross(a, b))

    return area


def tetra_volume(p1, p2, p3, p4) -> float:
    """Calculate the volume of a tetrahedron. Each point is an array of shape (3,)"""

    a = p2 - p1
    b = p3 - p1
    c = p4 - p1

    volume = (1 / 6) * norm(np.dot(a, np.cross(b, c)))

    return volume


def main(file: Path):
    ############################################################################
    # OPEN FILE AND READ X Y Z DATA

    points = read_cmm(file)

    ############################################################################
    # PERFORM TRIANGULATION

    # "simplices" is an array with rows that each contain 4 indices.
    # The indices refer to the point in the "points" array by position.
    simplices = Delaunay(points).simplices

    ############################################################################
    # CALCULATE VOLUME

    volume = 0

    for simplex in simplices:
        # Note that we need to get the actual coordinates from the "points"
        # array since "simplices" only contains indices.
        volume += tetra_volume(*(points[i] for i in simplex))

    print(f"{volume = :.2E} Å³")

    ############################################################################
    # CALCULATE SURFACE AREA

    triangles = []

    # First we need to get every triangle. The triangles are every combination
    # of 3 vertices found in each tetrahedron.
    for simplex in simplices:
        for triangle in combinations(simplex, 3):
            triangles.append(triangle)

    # The outer surface triangles are those that are only listed once.
    triangles = list(map(sorted, triangles))
    triangles = [t for t in triangles if triangles.count(t) == 1]

    surface_area = 0

    for triangle in triangles:
        surface_area += tri_area(*(points[i] for i in triangle))

    print(f"{surface_area = :.2E} Å²")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=Path)
    main(**vars(parser.parse_args()))
