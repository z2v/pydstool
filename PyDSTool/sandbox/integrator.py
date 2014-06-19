#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import scipy.integrate._ode as spode

from PyDSTool.sandbox import dopri


cdopri = dopri.dopri

vode = getattr(spode, 'vode', lambda: None)
lsoda = getattr(spode, 'lsoda', lambda: None)
dopri5 = getattr(spode, 'dopri5', lambda: None)
dop853 = getattr(spode, 'dop853', lambda: None)
