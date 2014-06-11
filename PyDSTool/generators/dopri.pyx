from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from libc.math cimport sin

cimport cdopri
import numpy as np
cimport numpy as np


cdef void c_vfield(unsigned n, double x, double* y_, double* p_, double* dydx):
    cdef int i
    for i from 0<= i < n:
        dydx[0] = y_[1]
        dydx[1] = -y_[0]
    return


cdef class dopri(object):
    cdef double* y

    def __cinit__(self):
        self.y = <double*> PyMem_Malloc(sizeof(double))
        if not self.y:
            raise MemoryError()

    def __dealloc__(self):
        PyMem_Free(self.y)

    def __init__(self):
        pass

    def Run(self, rhs):
        cdef int dim = 2
        self.y = <double*> PyMem_Realloc(self.y, dim * sizeof(double))
        if not self.y:
            raise MemoryError()

        self.y[0] = self.y[1] = 1.0

        cdef double rtoler = 1e-8
        cdef double atoler = 1e-6
        status = cdopri.dop853(
            dim, # n
            c_vfield, #fcn
            0.0, #x
            self.y, #y
            NULL,# pars
            1.0, #xend
            &rtoler,
            &atoler,
            0, # itoler
            NULL, # solout
            0, # iout
            NULL, # fileout
            0, # uround
            0, # safe,
            0, # fac1
            0, #fac2,
            0, # beta,
            0, #hmax,
            0, #h,
            0, #nmax,
            1, #meth
            0, #nstiff
            0, #nrdens
            NULL, #icont
            0, #licont
            0, #boundscheck
            0, #boundmaxsteps
            NULL, #magbound
            NULL #adjust_h
        )
        print("status: {0}, result: {1}".format(status, cdopri.xRead()))

        for i from 0 <= i < dim:
            print(self.y[i])
