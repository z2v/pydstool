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
def ode():
    t = linspace(0.0, 1.0, 25)
    ds, _ = oscillator(t)
    return Lsodar_ODEsystem(ds)


def test_lsodar_inherits_odesystem(ode):
    assert isinstance(ode, ODEsystem)
    assert 'x' in ode.variables
    assert 'xdot' in ode.variables
    assert 'x' in ode.funcspec.vars
    assert 'xdot' in ode.funcspec.vars


def test_lsodar_compute_returns_trajectory(ode):
    traj = ode.compute('traj')

    assert isinstance(traj, Trajectory)
    assert traj.name == 'traj'
    assert 'x' in traj(0.0)
    assert 'xdot' in traj(0.0)
    assert_almost_equal(ode.tdomain[0], traj.indepdomain[0])
    assert_almost_equal(ode.tdomain[1], traj.indepdomain[1])


def test_lsodar_compute_change_defined_status(ode):
    assert not ode.defined
    _ = ode.compute('_')
    assert ode.defined
