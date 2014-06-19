include 'generators.pxi'

cdef class VField:

    cpdef np.ndarray[DTYPE, ndim=1, negative_indices=False, mode='c'] rhs(self, double t, np.ndarray[DTYPE, ndim=1, negative_indices=False, mode='c'] x):
        return 0
