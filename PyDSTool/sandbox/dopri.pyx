include 'generators.pxi'

from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

cimport cdopri

cdef object f


cdef void c_vfield(unsigned n, double x, double* y_, double* p_, double* dydx):
    cdef int i
    cdef np.ndarray y

    y = np.zeros((n, ))

    for i from 0 <= i < n:
        y[i] = y_[i]

    global f
    yy = f(x, y)

    for i from 0 <= i < n:
        dydx[i] = yy[i]
    return


cdef class dopri(object):

    cdef double* y
    cdef int status
    cdef double xend
    cdef np.ndarray yend
    cdef object algparams

    cdef double rtol, atol, safety, dfactor, ifactor, beta, max_step, init_step
    cdef int dim
    cdef long nsteps
    cdef readonly int success

    def __cinit__(self):
        self.y = <double*> PyMem_Malloc(sizeof(double))
        if not self.y:
            raise MemoryError()

    def __dealloc__(self):
        PyMem_Free(self.y)

    def __init__(self,
                 double rtol=1e-6,
                 double atol=1e-12,
                 long nsteps=500,
                 double max_step=0.0,
                 double first_step=0.0,
                 double safety=0.9,
                 double ifactor=6.0,
                 double dfactor=0.3,
                 double beta=0.0,
                 ):

        self.status = 0
        self.xend = 0.0

        self.dim = 0

        self.atol = atol
        self.rtol = rtol
        self.safety = safety
        self.dfactor = dfactor
        self.ifactor = ifactor
        self.beta = beta
        self.max_step = max_step
        self.init_step = first_step
        self.nsteps = nsteps
        self.success = 0

    def reset(self, n, has_jac):
        self.dim = n
        self.y = <double*> PyMem_Realloc(self.y, n * sizeof(double))
        if not self.y:
            raise MemoryError()
        self.yend = np.zeros((n, ))

    def run(self, vf, jac, y0, t0, t1, f_params, jac_params):

        for i, v in enumerate(y0):
            self.y[i] = v

        global f
        f = vf

        self.status = cdopri.dop853(
            self.dim, # n
            c_vfield, #fcn
            t0, #x
            self.y, #y
            NULL,# pars
            t1, #xend
            &self.rtol,
            &self.atol,
            0, # itoler
            NULL, # solout
            0, # iout
            NULL, # fileout
            0.0, # uround
            self.safety, # safe,
            self.dfactor, # fac1
            self.ifactor, #fac2,
            self.beta, # beta,
            self.max_step, #hmax,
            self.init_step, #h,
            self.nsteps, #nmax,
            1, #meth
            0, #nstiff
            self.dim, #nrdens
            NULL, #icont
            0, #licont
            0, #boundscheck
            0, #boundmaxsteps
            NULL, #magbound
            NULL #adjust_h
        )
        self.xend = cdopri.xRead()
        self.success = self.status == 1

        for i from 0 <= i < self.dim:
            self.yend[i] = self.y[i]

        return (self.yend, self.xend)

    def get_stats_info(self):
        return {
            'last_step': cdopri.hRead(),
            'num_steps': cdopri.nstepRead(),
            'num_accept': cdopri.naccptRead(),
            'num_reject': cdopri.nrejctRead(),
            'num_fcns': cdopri.nfcnRead(),
            'errorStatus': self.status,
        }
