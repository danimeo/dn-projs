# cuda_neighbor_list.py

from numba import jit
from numba import cuda
import numpy as np


@jit
def neighbor_list(crd, neighbors, data_length, cutoff):
    for i in range(data_length):
        for j in range(i+1, data_length):
            if np.linalg.norm(crd[i]-crd[j]) <= cutoff:
                neighbors[i][j] = 1
                neighbors[j][i] = 1
    return neighbors


if __name__ == '__main__':
    import time
    np.random.seed(1)

    atoms = 2**5
    cutoff = 0.5
    crd = np.random.random((atoms, 3)).astype(np.float32)
    adjacent = np.zeros((atoms, atoms)).astype(np.float32)

    time0 = time.time()
    adjacent_c = neighbor_list(crd, adjacent, atoms, cutoff)
    time1 = time.time()
    print('The time cost of CPU with numba.jit is: {}s'.format(time1-time0))
