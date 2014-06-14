#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from numpy import sqrt, cos, sin
from numpy.testing import assert_almost_equal, assert_array_almost_equal

from PyDSTool.generators import dopri


k = 4.0
m = 1.0
y0 = [1.0, 0.1]


def oscillator(t, y):
    return [y[1], - k / m * y[0]]


def expected(t):
    omega = sqrt(k / m)
    return [
        y0[0] * cos(omega * t) + y0[1] * sin(omega * t) / omega,
        - y0[0] * omega * sin(omega * t) + y0[1] * cos(omega * t)
    ]


def test_cdopri_smoke():
    integrator = dopri.dopri()
    tend = 1.0
    (x, y) = integrator.Run(oscillator, y0, tspan=[0.0, tend])
    assert integrator.successful()
    assert_almost_equal(tend, x)
    assert_array_almost_equal(expected(tend), y)
