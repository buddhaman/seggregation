#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 22:45:09 2017

@author: timtrussner
"""
import numpy as np

def f(t, y):
    return np.array([y[1], -np.sin(y[0])])

def method(dt, t0, t1):
    t = t0
    y = np.array([0, 1])
    alpha = 100
    while t < t1:   
        y = y + dt*f(t+alpha*dt, y+alpha*dt*f(t, y))
        t+=dt
    return y

print method(0.1, 0, 0.1)
