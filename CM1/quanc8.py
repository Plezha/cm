import ctypes
from math import *

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


def f1(x):
    return abs(x - tan(x)) ** -0.5


def f2(x):
    return abs(x - tan(x)) ** -1


print('m\t\t', 'resultR\t\t\t', 'errestR\t\t\t', 'nofunR\t', 'posnR\t', 'flag', sep='')
print('-0.5\t',
      *quanc8_wrapper(
          ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(f1), 2.0, 5.0, 1e-6, 1e-6
      ),
      sep='\t')
print('-1\t',
      *quanc8_wrapper(
          ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(f2), 2.0, 5.0, 1e-6, 1e-6
      ),
      sep='\t')

print("""
eps\t first_part\t second_part\t sum""")
for eps in 1e-5, 1e-15, 0:
    first_part = quanc8_wrapper(
        ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(f2), 2.0, 4.49340945790906417530788093-eps, 1e-6, 1e-6
    )[0]
    second_part = quanc8_wrapper(
        ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(f2), 4.49340945790906417530788093+eps, 5, 1e-6, 1e-6
    )[0]
    print(f"{eps}\t %.6f\t %.6f\t %.6f" % (first_part, second_part, first_part + second_part))
