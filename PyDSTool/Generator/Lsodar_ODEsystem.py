#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyDSTool import Trajectory, Variable
from PyDSTool.common import interp1d
from PyDSTool.Generator import ODEsystem as ODEsystem
from baseclasses import theGenSpecHelper
from lsodar import lsodar


class Lsodar_ODEsystem(ODEsystem):

    def __init__(self, dsargs):
        super(Lsodar_ODEsystem, self).__init__(dsargs)

    def compute(self, name):
        self.defined = True
        points = [Variable(interp1d(self.tdomain, [0.0, 1.0]), 't', name=v)
                for v in self.variables]
        return Trajectory(name, points)


theGenSpecHelper.add(Lsodar_ODEsystem, {}, 'python')
