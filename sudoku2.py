import numpy as np
import pandas as pd
from knuth2 import exact_cover

p = [int(x) for x in (
    "010009000"
    "743002000"
    "000800102"
    "000000400"
    "000060050"
    "009001007"
    "005000060"
    "001000900"
    "000750801"
)]

p = np.array(p).reshape((9,9))
print(p,'\n')

A = np.zeros((729, 324), dtype=int)

row = 0
index = []
for i in range(9):
    for j in range(9):
        rng = [p[i,j]-1] if p[i,j] else range(9)
        for k in rng:
            A[row, 9*i + k] = 1
            A[row, 81 + 9*j + k] = 1
            A[row, 162 + 27*(i//3) + 9*(j//3) + k] = 1
            A[row, 243 + 9*i + j] = 1
            index.append("%d %d %d" % (i,j,k))
            row += 1
A = pd.DataFrame(A[:row,:], index=index)

solution = next(exact_cover(A))
m = np.zeros((9,9), dtype=int)
for s in solution:
    i, j, k = map(int, s.split())
    m[i, j] = k + 1
print (m)









