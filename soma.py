"""
Generate all solutions for the Soma cube puzzle, up to rotations.
(See https://en.wikipedia.org/wiki/Soma_cube)
The output is a csv file with one row for each solution.
Each row is a list of 27 integers between 1 and 7,
representing the seven different puzzle pieces.
A row is obtained by listing the entries of a 3x3x3 matrix
in lexicographic order:
a[0,0,0], a[0,0,1], a[0,0,2], a[0,1,0], ..., a[2,2,2].
"""

import numpy as np
import pandas as pd
from knuth import exact_cover

coords = [
    [(0,0,0), (1,0,0), (0,1,0)], # V
    [(0,0,0), (1,0,0), (2,0,0), (0,1,0)], # L
    [(0,0,0), (1,0,0), (2,0,0), (1,1,0)], # T
    [(0,0,0), (1,0,0), (1,1,0), (2,1,0)], # Z
    [(0,0,0), (1,0,0), (1,1,0), (1,1,1)], # A
    [(0,0,0), (1,0,0), (0,1,0), (0,1,1)], # B
    [(0,0,0), (1,0,0), (0,1,0), (0,0,1)]  # P
]

polycubes = []
for lst in coords:
    x = max(p[0] for p in lst) + 1
    y = max(p[1] for p in lst) + 1
    z = max(p[2] for p in lst) + 1
    A = np.zeros((x, y, z), dtype=int)
    for i, j, k in lst:
        A[i, j, k] = 1
    polycubes.append(A)


def rotate(A):
    def _rotate(A):
        for p in ((0,1,2), (1,2,0), (2,0,1)):
            B = np.transpose(A, p)
            yield B
            yield B[::-1, ::-1, :]
            yield B[::-1, :, ::-1]
            yield B[:, ::-1, ::-1]
        for p in ((0,2,1), (1,0,2), (2,1,0)):
            B = np.transpose(A, p)
            yield B[::-1, :, :]
            yield B[:, ::-1, :]
            yield B[:, :, ::-1]
            yield B[::-1, ::-1, ::-1]

    seen = set()
    for B in _rotate(A):
        s = str(B)
        if s not in seen:
            seen.add(s)
            yield B

def generate_rows():
    for index, poly in enumerate(polycubes):
        v = [0]*7
        v[index] = 1
        rotations = rotate(poly) if index != 1 else [poly]
        for A in rotations:
            x, y, z = A.shape
            for i in range(4-x):
                for j in range(4-y):
                    for k in range(4-z):
                        B = np.zeros((3,3,3), dtype=int)
                        B[i:i+x, j:j+y, k:k+z] = A
                        yield list(B.ravel()) + v

A = pd.DataFrame(generate_rows())
data = []

for row in exact_cover(A):
    v = np.zeros(27, dtype=int)
    for i, n in enumerate(sorted(row)):
        v += (i+1) * A.iloc[n] [:27]
    data.append(v)
pd.DataFrame(data).to_csv('soma.txt', index=False, header=False)