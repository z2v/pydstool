cimport numpy as np

cdef class VField:
    cpdef np.ndarray rhs(self, double t, np.ndarray x)

