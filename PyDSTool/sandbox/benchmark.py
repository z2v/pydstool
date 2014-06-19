#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from collections import defaultdict
import numpy as np
import timeit

from PyDSTool.sandbox import integrator as I

import pyximport
pyximport.install()

from oscillator import oscillator, oscillator_fun, Oscillator


k = 4.0
m = 1.0
y0 = [1.0, 0.1]
tend = 1000
algparams = {'nsteps': 1e6}
integrator = None


def oscillator_py(t, y, pars=None):
    return np.asarray([y[1], - k / m * y[0]])


def python_callback():
    integrator.run(oscillator_py, lambda t, y: None, y0, 0.0, tend, (None, ), (None, ))


def cython_callback_method():
    integrator.run(Oscillator().rhs, lambda t, y: None, y0, 0.0, tend, (None, ), (None, ))


def cython_callback_alias():
    integrator.run(oscillator, lambda t, y: None, y0, 0.0, tend, (None, ), (None, ))


def cython_callback_function():
    integrator.run(oscillator_fun, lambda t, y: None, y0, 0.0, tend, (None, ), (None, ))


def _format(t, fmt='{0:6.2f}{1:2s}'):
    usec = t * 1e6
    if usec < 1000.:
        return fmt.format(usec, 'ns')
    else:
        msec = usec / 1000.
        if msec < 1000:
            return fmt.format(msec, 'ms')
        else:
            sec = msec / 1000.
            return fmt.format(sec, 's')


if __name__ == '__main__':
    repeat = 5
    funcs = [python_callback, cython_callback_method, cython_callback_alias, cython_callback_function]
    modules = ['cdopri', 'dop853', 'dopri5', 'vode', 'lsoda']
    results = defaultdict(dict)

    for mod in modules:
        integrator = getattr(I, mod)(**algparams)
        for f in funcs:
            results[mod][f.__name__] = min(
                timeit.repeat(
                    f,
                    setup="from __main__ import integrator, y0; integrator.reset(len(y0), False)",
                    number=1,
                    repeat=repeat))

    print('{0:25s} | {1}'.format(
        '',
        ' | '.join(['{0:^8s}'.format(m) for m in modules])))

    sep = '-' * (25 + 11 * len(modules))
    print(sep)
    for f in funcs:
        print('{0:25s} | {1}'.format(
            f.__name__,
            ' | '.join([_format(results[m][f.__name__]) for m in modules])))
    print(sep)
    print('best time of {} tries'.format(repeat))
