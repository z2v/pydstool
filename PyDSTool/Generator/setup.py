#!/usr/bin/env python

import platform
from os.path import join, exists


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.system_info import get_info
    config = Configuration('Generator', parent_package, top_path)

    blas_opt = get_info('blas_opt', notfound_action=2)

    # Extra F2PY options
    f2py_opt = [
        #'--debug-capi',
        #'--verbose'
    ]

    # Extra complier args
    extra_args = [
        '-w',
        '-march=native',
        '-mtune=native',
        '-ftree-vectorize'
    ]

    # Extra F2PY macros
    f2py_macros = [
        #('F2PY_REPORT_ON_ARRAY_COPY', '1'),
        #('F2PY_REPORT_ATEXIT', '1'),
    ]

    config.add_library('lsodar',
                       sources=[join('..', 'integrator', 'lsodar', '*.f')],
                       extra_f77_compile_args=extra_args,
                       f2py_options=f2py_opt)

    libs = ['lsodar']

    # Remove libraries key from blas_opt
    if 'libraries' in blas_opt:    # key doesn't exist on OS X ...
        libs.extend(blas_opt['libraries'])
    newblas = {}
    for key in blas_opt.keys():
        if key == 'libraries':
            continue
        newblas[key] = blas_opt[key]

    newblas['define_macros'] = newblas['define_macros'] + f2py_macros

    config.add_extension('_lsodar',
                         sources=['lsodar.pyf'],
                         f2py_options=f2py_opt,
                         libraries=libs, **newblas)

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
