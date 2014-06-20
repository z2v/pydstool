#include <stdio.h>
#include <sys/time.h>

#include "dop853/dop853.h"

static double k = 4.0;
static double m = 1.0;

void oscillator(unsigned n, double x, double* y, double* p, double* f) {
    f[0] = y[1];
    f[1] = - k / m * y[0];
}


int run(unsigned n, FcnEqDiff vf, double* y0, double t0, double t1) {
    double rtol = 1e-6;
    double atol = 1e-12;

    return dop853(
        2,          /* dimension of the system <= UINT_MAX-1*                                                             */
        oscillator, /* function computing the value of f(x,y) *                                                           */
        t0,         /* initial x-value *                                                                                  */
        y0,         /* initial values for y *                                                                             */
        NULL,       /* vector field parameters *                                                                          */
        t1,         /* final x-value (xend-x may be positive or negative) *                                               */
        &rtol,      /* relative error tolerance *                                                                         */
        &atol,      /* absolute error tolerance *                                                                         */
        0,          /* switch for rtoler and atoler *                                                                     */
        NULL,       /* function providing the numerical solution during integration *                                     */
        0,          /* switch for calling solout *                                                                        */
        NULL,       /* messages stream *                                                                                  */
        0.0,        /* rounding unit *                                                                                    */
        0.9,        /* safety factor *                                                                                    */
        0.3,        /* parameters for step size selection *                                                               */
        6.0,
        0.0,        /* for stabilized step size control *                                                                 */
        0.0,        /* maximal step size *                                                                                */
        0.0,        /* initial step size *                                                                                */
        1e6,        /* maximal number of allowed steps *                                                                  */
        1,          /* switch for the choice of the coefficients *                                                        */
        0,          /* test for stiffness *                                                                               */
        2,          /* number of components for which dense outpout is required *                                         */
        NULL,       /* indexes of components for which dense output is required, >= nrdens *                              */
        0,          /* declared length of icon *                                                                          */
        0,          /* Flag for checking magbound not exceeded: 0 no checking; 1 check for initial boundmaxsteps steps; * */
        0,          /* number of initial steps for which to check magbound not exceeded *                                 */
        NULL,       /* bound on absolute value of components of the solution *                                            */
        NULL);      /* prevent h step from crossing external input times (if present) *                                   */
}


int main() {
    double y0[2];
    int status = 0;
    double t0 = 0.0;
    double t1 = 1000.0;
    int i;

    struct timeval tv1, tv2;
    struct timezone tz1, tz2;

    y0[0] = 1.0;
    y0[1] = 0.1;
    gettimeofday(&tv1, &tz1);
    status = run(2, oscillator, y0, t0, t1);
    gettimeofday(&tv2, &tz2);
    printf("Integration lasted %.3f milliseconds\n", ((tv2.tv_sec - tv1.tv_sec) * 1000000 + (tv2.tv_usec - tv1.tv_usec)) / 1000.);

    printf("%15.0f", xRead());
    for(i=0; i < 2; i++) {
        printf("%15.8f", y0[i]);
    }
    printf("\n");

    printf("nfunc = %ld\n", nfcnRead());
    return status == 1 ? 0 : 1;
}
