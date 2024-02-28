import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


def lagrange_polynomial(x, y):
    def L(k):
        return lambda x_val: np.prod([(x_val - x[j]) / (x[k] - x[j]) for j in range(len(x)) if j != k])

    return lambda x_val: np.sum(y[k] * L(k)(x_val) for k in range(len(x)))


def f(x):
    return 1 / (1 + x)


x = np.array([.1 * i for i in range(0, 11)])
y = np.array([f(x) for x in x])

poly = lagrange_polynomial(x, y)
spline = CubicSpline(x, y)

points = np.linspace(0.05, 0.95, 10)
# Plot data points
plt.scatter(points, [0.5] * 10, color='red', label='Data Points')

# Plot given function interpolation
plt.plot(points, [f(x) for x in points], label='f(x)')

# Plot Lagrange polynomial interpolation
plt.plot(points, [poly(x) for x in points], label='Lagrange Interpolation')

# Plot cubic spline interpolation
plt.plot(points, [spline(x) for x in points], label='Cubic Spline Interpolation')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Lagrange vs. Cubic Spline Interpolation')
plt.grid(True)
plt.figure()

# Plot data points
plt.scatter(points, [0.0] * 10, color='red', label='Data Points')

# Plot Lagrange polynomial errors
plt.plot(points, [1000*(f(x) - poly(x)) for x in points], label='1000х Lagrange Errors')

# Plot cubic spline errors
plt.plot(points, [f(x) - spline(x) for x in points], label='Cubic Spline Errors')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Lagrange vs. Cubic Spline Interpolation Errors')
plt.grid(True)
plt.show()
