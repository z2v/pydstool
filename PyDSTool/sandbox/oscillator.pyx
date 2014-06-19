# cython: cdivision=True
# cython: boundscheck=False
import numpy as np
cimport numpy as np

cdef double k = 4.0
cdef double m = 1.0

# ===== As an object method
cdef class Oscillator:
    cdef np.ndarray dydt

    def __init__(self):
        self.dydt = np.zeros((2, ))

    cpdef np.ndarray rhs(self, double t, np.ndarray y, tuple pars=()):
        global k, m
        self.dydt[0] = y[1]
        self.dydt[1] = - k / m * y[0]
        return self.dydt



# ==== As an alias to bject method
cdef Oscillator O = Oscillator()

cpdef np.ndarray oscillator(double t, np.ndarray y, tuple pars=()):
    return O.rhs(t, y, pars)


# ===== As a function with globally set result array
cdef np.ndarray dydt = np.zeros((2, ))

cpdef np.ndarray oscillator_fun(double t, np.ndarray y, tuple pars=()):
    global dydt, k, m
    dydt[0] = y[1]
    dydt[1] = - k / m * y[0]
    return dydt
