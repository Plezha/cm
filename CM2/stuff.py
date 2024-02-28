import numpy as np


def init_H(a):
    return np.array([
        [a, 1, 0, 0],
        [a ** 2, a, 1, 0],
        [a ** 3, a ** 2, a, 1],
        [a ** 4, a ** 3, a ** 2, a]
    ], dtype='d')


def init_A(a, b):
    h = init_H(a)

    h[1, 2] += 0.1
    for i in 0, 1, 2, 3:
        h[i, i] += b

    return h


def norm(A):
    return max([abs(sum(i)) for i in A])


for b in 0.1, 1e-2, 1e-3:
    print(f"{b = }")
    A = init_A(2, b)

    inverted_A = np.linalg.inv(A)
    kinda_E = np.dot(A, inverted_A)

    R = kinda_E
    for i in 0, 1, 2, 3:
        R[i, i] -= 1
    det_A = np.linalg.det(A)
    cond_A = norm(A) * norm(inverted_A)
    print(f"{R = }", f"{det_A = }", f"{norm(R) = }", f"{cond_A = }", sep='\n')
    print()
