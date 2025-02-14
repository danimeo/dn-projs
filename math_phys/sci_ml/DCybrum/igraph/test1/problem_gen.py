
import matplotlib.pyplot as plt
import numpy as np
import random


def get_fig(n=10, index=0, description=''):
    X = np.random.normal(0, 0.7, n)
    Y = np.random.normal(0, 0.7, n)

    broke = True
    while broke:
        broke = False
        X = np.random.normal(0, 0.7, n)
        Y = np.random.normal(0, 0.7, n)
        for i1 in range(n):
            for i2 in range(i1, n):
                if i1 != i2 and ((X[i1]-X[i2])**2 + (Y[i1]-Y[i2])**2)**0.5 < 0.22:
                    broke = True
                    break
            if broke:
                break

    plt.scatter(X, Y, s=150, alpha=.7)

    plt.xlim((-2, 2))
    plt.xticks([])  # ignore xticks
    plt.ylim((-2, 2))
    plt.yticks([])  # ignore yticks
    # plt.show()
    plt.savefig(f'img/{description}_{index}_{n}.png')
    plt.close()


for i in range(100):
    print(i)
    a = random.randint(1, 4)
    b = random.randint(1, 4)
    c = random.randint(2, 8)
    get_fig(a, i, 'a')
    get_fig(b, i, 'b')
    get_fig(c, i, 'c')
