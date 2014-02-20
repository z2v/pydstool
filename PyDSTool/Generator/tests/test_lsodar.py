#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from numpy import linspace
from numpy.testing import assert_almost_equal
import pytest

from PyDSTool import Interval, Trajectory
from PyDSTool.Generator import lsodar, Lsodar_ODEsystem, ODEsystem
from PyDSTool.Generator.tests.samples import oscillator


def test_smoke():
    assert lsodar.__doc__ != ''


@pytest.fixture
def dsargs():
    t = linspace(0.0, 1.0, 25)
    ds, _ = oscillator(t)
    return ds


def test_lsodar_inherits_odesystem(dsargs):
    ode = Lsodar_ODEsystem(dsargs)
    assert isinstance(ode, ODEsystem)
    assert 'x' in ode.variables
    assert 'xdot' in ode.variables
    assert 'x' in ode.funcspec.vars
    assert 'xdot' in ode.funcspec.vars


def test_lsodar_compute_returns_trajectory(dsargs):
    ode = Lsodar_ODEsystem(dsargs)
    traj = ode.compute('traj')

    assert isinstance(traj, Trajectory)
    assert traj.name == 'traj'
    assert 'x' in traj(0.0)
    assert 'xdot' in traj(0.0)
    assert_almost_equal(ode.tdomain[0], traj.indepdomain[0])
    assert_almost_equal(ode.tdomain[1], traj.indepdomain[1])


def test_lsodar_compute_change_defined_status(dsargs):
    ode = Lsodar_ODEsystem(dsargs)

    assert not ode.defined
    _ = ode.compute('_')
    assert ode.defined
