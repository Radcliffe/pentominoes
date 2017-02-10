import pandas as pd
import numpy as np
from knuth import exact_cover

pentominoes = [
    np.array(p) for p in [

        # F
        [[0,1,1],  
         [1,1,0],
         [0,1,0]],
        
        # I
        [[1,1,1,1,1]],
        
        # L
        [[1,1,1,1],
         [0,0,0,1]],
        
        # N
        [[1,1,0,0],
         [0,1,1,1]],
        
        # P
        [[1,1,1],
         [0,1,1]],
        
        # T
        [[1,1,1],
         [0,1,0],
         [0,1,0]],
        
        # U
        [[1,0,1],
         [1,1,1]],
        
        # V
        [[1,0,0],
         [1,0,0],
         [1,1,1]],
        
        # W
        [[1,0,0],
         [1,1,0],
         [0,1,1]],
        
        # X
        [[0,1,0],
         [1,1,1],
         [0,1,0]],
        
        # Y
        [[0,0,1,0],
         [1,1,1,1]],
        
        # Z
        [[1,1,0],
         [0,1,0],
         [0,1,1]]
    ]
]

def all_orientations(A, i):
    """Generate all distinct orientations of the pentominoes,
    including rotations and reflections."""

    # Fixing the orientation of the first (F) pentomino eliminates
    # redundant solutions resulting from rotations or reflections."""
    if i == 0:
        yield A
        return
        
    seen = set()
    # Apply transpose, left/right flip, and up/down flip in all combinations
    # to generate all possible orientiations of a pentomino.
    for A in (A, A.T):
        for A in (A, np.fliplr(A)):
            for A in (A, np.flipud(A)):
                s = str(A)
                if not s in seen:
                    yield A
                    seen.add(s)


def all_positions(A, i):
    """ Find all positions to place the pentominoes. """
    for A in all_orientations(A, i):
        rows, cols = A.shape
        for i in range(9 - rows):
            for j in range(9 - cols):
                M = np.zeros((8, 8), dtype='int')
                M[i:i+rows, j:j+cols] = A
                if M[0,0] == M[0,7] == M[7,0] == M[7,7] == 0:
                    yield np.delete(M.reshape(64), [0, 7, 56, 63])

rows = []
for i, P in enumerate(pentominoes):
    for A in all_positions(P, i):
        A = np.append(A, np.zeros(12, dtype='int'))
        A[60+i] = 1
        rows.append(list(A))

A = pd.DataFrame(rows)
A.to_csv('matrix.csv')
covers = np.array(list(exact_cover(A)), dtype='int')
np.savetxt('exact-covers.csv', covers, delimiter=',', fmt='%d')
print ('Time: %.2f seconds' % (time() - start_time))