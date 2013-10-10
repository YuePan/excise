import numpy as np 
import matplotlib.pyplot as pl
a = 1
b = 2
c = 3

class A(object):
    pass


class B(object):
    pass


class C(A):
    pass

class D(object):
    """docstring for D"""
    def __init__(self, arg):
        super(D, self).__init__()
        self.arg = arg

