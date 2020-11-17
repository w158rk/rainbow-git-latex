#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   util.py
@Time    :   2020/11/17 20:04:46
@Author  :   Kyle Wang
@Version :   1.0
@Contact :   wrk15835@gmail.com
@License :   (C)Copyright 2020-2021, Kyle Wang
@Desc    :   None
'''

SKIP_ENVS = [
    "figure",
    "table"
]

SKIP_COMMANDS = [
    "\\import"
]

SKIP_ENVS = set(SKIP_ENVS)
SKIP_COMMANDS = set(SKIP_COMMANDS)