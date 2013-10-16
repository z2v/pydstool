#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyDSTool.Generator import lsodar


def test_smoke():
    assert lsodar.__doc__ != ''
