#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/3/18'
# qq:2456056533

"""

import execjs


def runjs(js_file, func_name, *args):
    with open(js_file, 'r') as f:
        js = f.read()

    ctx = execjs.compile(js)
    # ctx.call("show", " ")
    ctx.call(func_name, *args)

