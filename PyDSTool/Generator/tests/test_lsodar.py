#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import linspace
import pytest

from PyDSTool.Generator import lsodar, Lsodar_ODEsystem, ODEsystem

from samples import oscillator


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
