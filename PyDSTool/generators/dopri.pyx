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
    cdef object algparams

    def __cinit__(self):
        self.y = <double*> PyMem_Malloc(sizeof(double))
        if not self.y:
            raise MemoryError()

    def __dealloc__(self):
        PyMem_Free(self.y)

    def __init__(self):
        self.status = 0
        self.xend = 0

        self.algparams = {
            'rtol': 1e-8,
            'atol': 1e-6,

            # by default set to 0, so default values will be used
            'uround': 0.0,
            'safety': 0.0,
            'fac1': 0.0,
            'fac2': 0.0,
            'beta': 0.0,
            'max_step': 0.0,
            'init_step': 0.0,
            'maxsteps': 0.0,

            # not available outside
            'meth': 1,
            'nstiff': 0,
        }

    def Run(self, rhs, y0, tspan=[0.0, 1.0], **kwargs):
        cdef int dim = len(y0)
        self.y = <double*> PyMem_Realloc(self.y, dim * sizeof(double))
        if not self.y:
            raise MemoryError()

        for i, v in enumerate(y0):
            self.y[i] = v

        global f
        f = rhs

        cdef double rtoler = kwargs.get('rtol', self.algparams['rtol'])
        cdef double atoler = kwargs.get('atol', self.algparams['atol'])
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
            kwargs.get('uround', self.algparams['uround']), # uround
            kwargs.get('safety', self.algparams['safety']), # safe,
            kwargs.get('fac1', self.algparams['fac1']), # fac1
            kwargs.get('fac2', self.algparams['fac2']), #fac2,
            kwargs.get('beta', self.algparams['beta']), # beta,
            kwargs.get('max_step', self.algparams['max_step']), #hmax,
            kwargs.get('init_step', self.algparams['init_step']), #h,
            kwargs.get('maxsteps', self.algparams['maxsteps']), #nmax,
            self.algparams['meth'], #meth
            self.algparams['nstiff'], #nstiff
            dim, #nrdens
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

    def get_stats_info(self):
        return {
            'last_step': cdopri.hRead(),
            'num_steps': cdopri.nstepRead(),
            'num_accept': cdopri.naccptRead(),
            'num_reject': cdopri.nrejctRead(),
            'num_fcns': cdopri.nfcnRead(),
            'errorStatus': self.status,
        }
