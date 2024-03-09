import numpy as np

from scipy import integrate
from scipy.optimize import fsolve


def ans(t):
    return t * t + 1


def rk45(f, T, Y0):
    r = integrate.ode(f).set_integrator('dopri5', atol=1e-6)
    r.set_initial_value(Y0, T[0])

    Y = np.zeros((len(T), len(Y0)))
    Y[0] = Y0

    for i in range(1, len(T)):
        Y[i] = r.integrate(T[i])

    return Y


def backward_euler(f, T, Y0):
    Y = np.zeros((len(T), len(Y0)))
    Y[0] = Y0
    for i in range(1, len(T)):
        f1 = lambda Y: f(T[i], Y)
        
        def equations(X):
            return [
                Y[i-1][j] + (T[i]-T[i-1]) * f1(X)[j] - X[j] for j in range(len(X))
                ]
        
        root = fsolve(equations, [0]*len(Y0), xtol=1e-14, maxfev=2**30)    
        for j in range(len(Y[i])):
            Y[i][j] = Y[i-1][j] + (T[i]-T[i-1])*f1(root)[j]
            
    return Y
    

def f(t, Y):
    dY = np.zeros(len(Y))
    dY[0] = Y[1]
    dY[1] = (2 * t * Y[1] - 2 * Y[0]) / (t ** 2 - 1)
    return dY


for h in 0.1, 0.05, 0.025, 0.0125:
    print(f"{h = }:")
    rng = np.arange(2, 3 + h - 1e-9, h)
    n_steps = len(rng)
    Y0 = [5, 4]
    res_rk45 = [i[0] for i in rk45(f, rng, Y0)]
    res_be = [i[0] for i in backward_euler(f, rng, Y0)]
    res_precise = [ans(rng[i]) for i in range(n_steps)]
    if h == 0.1:
        print("t\t\t rk45\t\t\t backward euler\t\t precise")
        for i in range(n_steps):
            print(f"{rng[i]:.8f}\t {res_rk45[i]:.16f}\t {res_be[i]:.16f}\t {res_precise[i]:.8f}")
    
    rk45_avg_error = sum([abs(res_rk45[i] - res_precise[i]) for i in range(n_steps)]) / n_steps 
    be_avg_error = sum([abs(res_be[i] - res_precise[i]) for i in range(n_steps)]) / n_steps 
    
    print(f"Avg. err.:\t {rk45_avg_error:.16f}\t {be_avg_error:.16f}")
    
    
