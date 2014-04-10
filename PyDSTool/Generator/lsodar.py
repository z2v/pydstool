#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, absolute_import, print_function

"""
lsodar
~~~~~~
    ODE solver with authomatic method switching for stiff (adams method)
    and nonstiff (bdf method) and root-finding.


    This integrator accepts the following parameters in set_integrator()
    method of the ode class:

    - atol  : float or sequence
      absolute tolerance for solution
    - rtol  : float or sequence
      relative tolerance for solution
    - lband : None or int
    - rband : None or int
      Jacobian band width, jac[i,j] != 0 for i-lband <= j <= i+rband.
      Setting these requires your jac routine to return the jacobian
      in packed format, jac_packed[i-j+lband, j] = jac[i,j].
    - nsteps : int
      Maximum number of (internally defined) steps allowed during one
      call to the solver.
    - first_step : float
    - min_step : float
    - max_step : float
      Limits for the step sizes used by the integrator.
    - order_adams : int
      order_bdf   : int
      Maximum order used by the integrator,
      order <= 12 for Adams, <= 5 for BDF.
    - g : None or function returning a sequence of floats
      The constraint function, whose roots should be found.
      t and y are passed as parameters to it.
      lsodar will stop integrating once at least one root of g
      is found.
    - ng : int
      Number of constraints -- i.e. length of the sequence
      returned by g.
"""

import warnings

try:
    from scipy.integrate._ode import IntegratorBase
except ImportError:
    from scipy.integrate.ode import IntegratorBase
from numpy import zeros, int32

from . import _lsodar

class lsodar(IntegratorBase):

    runner = getattr(_lsodar, 'dlsodar', None)

    messages = {-1: 'Excess work done on this call. (Perhaps wrong MF.)',
                -2: 'Excess accuracy requested. (Tolerances too small.)',
                -3: 'Illegal input detected. (See printed message.)',
                -4: 'Repeated error test failures. (Check all input.)',
                -5: 'Repeated convergence failures. (Perhaps bad'
                ' Jacobian supplied or wrong choice of MF or tolerances.)',
                -6: 'Error weight became zero during problem. (Solution'
                ' component i vanished, and ATOL or ATOL(i) = 0.)'
                }
    supports_run_relax = 1
    supports_step = 1

    def __init__(self,
                 rtol=1e-6,
                 atol=1e-12,
                 lband=None,
                 uband=None,
                 order_adams=12,
                 order_bdf=6,
                 nsteps=500,
                 max_step=0.0,      # corresponds to infinite
                 min_step=0.0,
                 first_step=0.0,    # determined by solver
                 ng=0,
                 g=lambda: None
                 ):

        call_args = {}
        call_args['rtol'] = rtol
        call_args['atol'] = atol
        call_args['ng'] = ng
        call_args['g'] = g
        self.call_args = call_args

        self.mu = uband
        self.ml = lband
        self.order_adams = order_adams
        self.order_bdf = order_bdf
        self.nsteps = nsteps
        self.max_step = max_step
        self.min_step = min_step
        self.first_step = first_step
        self.success = 1

    def reset(self, n, has_jac):
        # Calculate parameters for lsodar.
        ca = self.call_args
        if has_jac:
            if self.mu is None and self.ml is None:
                jt = 1
            else:
                if self.mu is None:
                    self.mu = 0
                if self.ml is None:
                    self.ml = 0
                jt = 4
        else:
            if self.mu is None and self.ml is None:
                jt = 2
            else:
                if self.mu is None:
                    self.mu = 0
                if self.ml is None:
                    self.ml = 0
                jt = 5

        ca['jt'] = jt

        lrw = 22 + n * max(16, n + 9) + 3 * ca['ng']
        rwork = zeros((lrw,), float)
        rwork[4] = self.first_step
        rwork[5] = self.max_step
        rwork[6] = self.min_step
        ca['rwork'] = rwork

        liw = 20 + n
        iwork = zeros((liw,), int32)
        if self.ml is not None:
            iwork[0] = self.ml
        if self.mu is not None:
            iwork[1] = self.mu
        #iwork[4]    = switch_debug
        iwork[5] = self.nsteps
        #iwork[6]    = num_messages
        iwork[7] = self.order_adams
        iwork[8] = self.order_bdf
        ca['iwork'] = iwork
        ca['istate'] = 1
        ca['itask'] = 1
        self.success = 1

    def run(self, f, jac, y, t, tout, f_params, jac_params):
        ca = self.call_args
        y1, t, istate, jroot = self.runner(f, jac, y, t, tout, ca['rtol'], ca['atol'], ca['itask'],
                                           ca['istate'], ca['rwork'], ca['iwork'], ca['jt'], ca['g'], ca['ng'])
        if istate < 0:
            warnings.warn('lsodar: ' +
                          self.messages.get(istate, 'Unexpected istate=%s' % istate))
            self.success = 0
        elif istate == 3:
            self.success = 0
        else:
            ca['istate'] = 2
        return y1, t

    def step(self, *args):
        itask = self.call_args['itask']
        self.call_args['itask'] = 2
        r = self.run(*args)
        self.call_args['itask'] = itask
        return r

    def run_relax(self, *args):
        itask = self.call_args['itask']
        self.call_args['itask'] = 3
        r = self.run(*args)
        self.call_args['itask'] = itask
        return r

    @property
    def infodict(self):
        """
        infodict: dict
           Dictionary containing additional output information

        =======  ============================================================
        key      meaning
        =======  ============================================================
        'hused'  The step size last used (successfully)
        'hcur'   The step size to attempted on the next step
        'nst'    The number of steps taken since last initialization
        'nfe'    The number of evaluations of the right hand side
        'nge'    The number of evaluations of the root function
        'nje'    The number of evaluations of the Jacobian matrix
        'nqused' The order last used (successfully)
        'nqcur'  The order to be attempted on the next step
        'mused'  The method used for the last successful step
        'mcur'   The method to be attempted for the next step
        """

        return {
            'hused': (
                self.rwork[11 - 1],
                'The step size last used (successfully)'
            ),
            'hcur': (
                self.rwork[12 - 1],
                'The step size to attempted on the next step'
            ),
            'nst': (
                self.iwork[11 - 1],
                'The number of steps taken since last initialization'
            ),
            'nfe': (
                self.iwork[12 - 1],
                'The number of evaluations of the right hand side'
            ),
            'nge': (
                self.iwork[10 - 1],
                'The number of evaluations of the root function'
            ),
            'nje': (
                self.iwork[13 - 1],
                'The number of evaluations of the Jacobian matrix'
            ),
            'nqused': (
                self.iwork[14 - 1],
                'The order last used (successfully)'
            ),
            'nqcur': (
                self.iwork[15 - 1],
                'The order to be attempted on the next step'
            ),
            'mused': (
                'adams (nonstiff)' if self.iwork[19 - 1] == 1 else 'BDF (stiff)',
                'The method used for the last successful step'
            ),
            'mcur': (
                'adams (nonstiff)' if self.iwork[20 - 1] == 1 else 'BDF (stiff)',
                'The method to be attempted for the next step'
            ),
        }

if lsodar.runner is not None:
    IntegratorBase.integrator_classes.append(lsodar)

