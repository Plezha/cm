import ctypes
from math import *
from random import random

import matplotlib.pyplot as plt
from scipy.optimize import fmin, fsolve
from scipy import integrate

C = 0
# Load the shared library
lib = ctypes.CDLL('./common/quanc8.dll')

# Define the argument types and return type of the quanc8 function
lib.quanc8.argtypes = [ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double),
                       ctypes.c_double, ctypes.c_double, ctypes.c_double,
                       ctypes.c_double, ctypes.POINTER(ctypes.c_double),
                       ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int),
                       ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int)]
lib.quanc8.restype = ctypes.c_int
    
    
def quanc8_wrapper(fun, a, b, abserr, relerr):
    resultR = ctypes.c_double()
    errestR = ctypes.c_double()
    nofunR = ctypes.c_int()
    posnR = ctypes.c_double()
    flag = ctypes.c_int()

    lib.quanc8(fun, a, b, abserr, relerr, resultR, errestR, nofunR, posnR, flag)

    return resultR.value, errestR.value, nofunR.value, posnR.value, flag.value


def getL():
    def f(x):
        return cos(x) / x

    return 0.4674158 * quanc8_wrapper(
        ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(f),
        1, 2, 1e-12, 1e-12)[0]


def getRR2E2():
    def equations(arr):
        R, R2, E2 = arr
        return [
            53 * R + 46 * R2 + 20 * E2 - 3060,
            46 * R + 50 * R2 + 26 * E2 - 2866,
            20 * R + 26 * R2 + 17 * E2 - 1337,
        ]

    root = fsolve(equations, [0] * 3, xtol=1e-14, maxfev=2 ** 30)
    return root


def getE1():
    def f(x):
        return abs(.6 ** x - x)

    xs = fmin(f, 0.8, xtol=1e-16, ftol=1e-16, disp=0)
    return 5.718088 * xs[0]


L = getL()
R, R2, E2 = getRR2E2()
E1 = getE1()
#print(f"{L = }\n{R = }\n{R2 = }\n{E2 = }\n{E1 = }\n")

tList = [i/1000 for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]
UcList = [-1.000, 7.777, 12.017, 10.701, 5.407, -0.843, -5.159, -6.015, -3.668, 0.283, 3.829]


def equations(t, iiU):
    global C
    i1, i3, Uc = iiU
    return [
        (E1 - E2 - Uc + i3*R2 - i1*(R + R2))/L,
        (E2 + Uc + i1*R2 - i3*(R2 + R))/L,
        (i1-i3)/C
    ]


def solve(UcList, showGraph=True):
    global C
    pairs = []
    for C_ in range(50, 201):
        C = C_
        C /= 100*1e6
    
        r = integrate.ode(equations).set_integrator('dopri5', nsteps=10000, atol=1e-7)
        iiU = [[E1/R, 0, UcList[0]]]
        r.set_initial_value(iiU[0], tList[0])
        
        for i in range(1, len(tList)):
            res = r.integrate(tList[i])
            iiU += [res]
    
        pairs += [(C, sum(abs(UcList[i] - iiU[i][2]) for i in range(len(tList))) / len(tList))]
        
    x_values = [pair[0] for pair in pairs]
    y_values = [pair[1] for pair in pairs]
    
    if showGraph:
        plt.plot(x_values, y_values, linestyle='-')
        plt.xlabel('C, μF')
        plt.ylabel('Average difference from experimental data, V')
        plt.title('Average difference from experimental data')
        plt.grid(True)
        plt.show()
    
    return min(pairs, key=lambda x: x[1])[0]


for orderOfError in [9, 5, 3, 2, 1, 0, -1, -2]:
    UcListWithErrors = [i + [-1, 1][random() > 0.5] * random() * 10**-orderOfError for i in UcList]
    print(orderOfError, solve(UcList=UcListWithErrors, showGraph=False), sep="\t")
