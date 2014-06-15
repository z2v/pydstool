from libc.stdio cimport FILE

cdef extern from "dop853.h":
    ctypedef void (*FcnEqDiff)(unsigned n, double x, double *y, double *p, double *f)
    ctypedef void (*SolTrait)(long nr, double xold, double x, double* y, unsigned n, int* irtrn)
    ctypedef void (*StepAdjuster) (double t, double* h)

    int dop853 (unsigned n,
      FcnEqDiff fcn,
      double x,
      double* y,
      double* pars,
      double xend,
      double* rtoler,
      double* atoler,
      int itoler,
      SolTrait solout,
      int iout,
      FILE* fileout,
      double uround,
      double safe,
      double fac1,
      double fac2,
      double beta,
      double hmax,
      double h,
      long nmax,
      int meth,
      long nstiff,
      unsigned nrdens,
      unsigned* icont,
      unsigned licont,
      int boundscheck,
      int boundmaxsteps,
      double *magbound,
      StepAdjuster adjust_h
     )

    double xRead()

    # statistical data
    long nfcnRead()
    long nstepRead()
    long naccptRead()
    long nrejctRead()
    double hRead()
