#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from _distfix import *

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.system_info import get_info
    config = Configuration('generators', parent_package, top_path)

    dop853_dir = 'dop853'
    config.add_include_dirs(dop853_dir)
    config.add_library(
        'dop853',
        sources=[os.path.join(dop853_dir, 'dop853.c')],
        depends=[os.path.join(dop853_dir, 'dop853.h')])

    config.add_extension(
        'dopri',
        sources=['dopri.pyx'],
        libraries=['dop853'])

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
