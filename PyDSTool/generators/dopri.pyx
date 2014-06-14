from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

cimport cdopri


cdef object f


cdef void c_vfield(unsigned n, double x, double* y_, double* p_, double* dydx):
    cdef int i

    y = []
    for i from 0 <= i < n:
        y.append(y_[i])

    global f
    yy = f(x, y)

    for i from 0 <= i < n:
        dydx[i] = yy[i]
    return


cdef class dopri(object):

    cdef double* y
    cdef int status
    cdef double xend

    def __cinit__(self):
        self.y = <double*> PyMem_Malloc(sizeof(double))
        if not self.y:
            raise MemoryError()

    def __dealloc__(self):
        PyMem_Free(self.y)

    def __init__(self):
        self.status = 0
        self.xend = 0

    def Run(self, rhs, y0, tspan=[0.0, 1.0]):
        cdef int dim = len(y0)
        self.y = <double*> PyMem_Realloc(self.y, dim * sizeof(double))
        if not self.y:
            raise MemoryError()

        for i, v in enumerate(y0):
            self.y[i] = v

        global f
        f = rhs

        cdef double rtoler = 1e-8
        cdef double atoler = 1e-6
        self.status = cdopri.dop853(
            dim, # n
            c_vfield, #fcn
            tspan[0], #x
            self.y, #y
            NULL,# pars
            tspan[-1], #xend
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
        self.xend = cdopri.xRead()

        yend = []
        for i from 0 <= i < dim:
            yend.append(self.y[i])

        return (self.xend, yend)

    def successful(self):
        return self.status == 1
