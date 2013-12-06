#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyDSTool.Generator import ODEsystem as ODEsystem
from baseclasses import theGenSpecHelper
from lsodar import lsodar


class Lsodar_ODEsystem(ODEsystem):

    def __init__(self, dsargs):
        super(Lsodar_ODEsystem, self).__init__(dsargs)

    def compute(self, name):
        self.defined = True


theGenSpecHelper.add(Lsodar_ODEsystem, {}, 'python')
