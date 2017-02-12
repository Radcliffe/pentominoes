# Knuth's Algorithm X

# 1. If the matrix A has no columns, the current partial solution is a valid solution; 
#    terminate successfully.
# 2. Otherwise choose a column c (deterministically).
# 3. Choose a row r such that A[r,c] = 1 (nondeterministically).
# 4. Include row r in the partial solution.
# 5. For each column j such that A[r,j] = 1,
#     for each row i such that A[i,j] = 1,
#         delete row i from matrix A.
#     delete column j from matrix A.
# 6. Repeat this algorithm recursively on the reduced matrix A.

def exact_cover(A):
    if A.shape[1] == 0:
        yield []                                    # Matrix has no columns; terminate successfully.
    else:
        c = A.sum(axis=0).argmin()                  # Choose a column c with the fewest 1s.
        for r in A.index[A[c] == 1]:                # For each row r such that A[r,c] = 1,
            B = A
            for j in A.columns[A.loc[r] == 1]:      #   For each column j such that A[r,j] = 1,
                B = B[B[j] == 0]                    #     Delete each row i such that A[i,j] = 1
                del B[j]                            #     then delete column j.
            for partial_solution in exact_cover(B):
                yield [r] + partial_solution        # Include r in the partial solution.
