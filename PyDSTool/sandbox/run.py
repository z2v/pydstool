#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import subprocess


if subprocess.call(['cc', '-O2', 'osc.c', 'dop853/dop853.c', '-lm']) == 0:
    times = []
    nfun = []
    for j in range(100):
        out = subprocess.check_output(['./a.out'], universal_newlines=True)
        for l in out.split('\n'):
            if 'milliseconds' in l:
                times.append(float(re.findall(r'\d+.\d{3}', l)[0]))
            if 'nfunc' in l:
                nfun.append(int(re.findall(r'\d+', l)[0]))

    print(sorted(zip(times, nfun))[0])

