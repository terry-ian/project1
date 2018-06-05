# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 09:21:40 2018

@author: terry_ian
"""

import os

def get_env_variable(var):
    try:
        return os.environ[var]
    except KeyError:
        print("Environment var '%s' not found." % var)

