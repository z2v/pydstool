#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from numpy import sqrt, cos, sin, asarray
from numpy.testing import assert_almost_equal, assert_array_almost_equal

from PyDSTool.sandbox import vfield
from PyDSTool.sandbox import integrator as I


k = 4.0
m = 1.0
y0 = [1.0, 0.1]


class Oscillator(vfield.VField):

    def rhs(self, t, y, pars=None):
        return asarray([y[1], - k / m * y[0]])


def expected(t):
    omega = sqrt(k / m)
    return [
        y0[0] * cos(omega * t) + y0[1] * sin(omega * t) / omega,
        - y0[0] * omega * sin(omega * t) + y0[1] * cos(omega * t)
    ]


def test_cdopri_smoke():
    integrator = _check_integrator(I.cdopri())

    stats_info = integrator.get_stats_info()
    assert stats_info['errorStatus'] == 1
    assert stats_info['last_step'] > 0
    assert stats_info['num_reject'] + stats_info['num_accept'] == stats_info['num_steps']


def test_scipy_dopri5():
    _check_integrator(I.dopri5())


def test_scipy_dop853():
    _check_integrator(I.dop853())


def test_scipy_lsoda():
    _check_integrator(I.lsoda())


def test_scipy_vode():
    _check_integrator(I.vode())


def _check_integrator(integrator):
    if integrator is None:
        return

    integrator.reset(len(y0), False)
    tend = 10.0
    (y, x) = integrator.run(Oscillator().rhs, lambda t, y: None, y0, 0.0, tend, (None, ), (None, ))

    assert integrator.success == 1
    assert_almost_equal(tend, x)
    assert_array_almost_equal(expected(tend), y, 4)

    return integrator
