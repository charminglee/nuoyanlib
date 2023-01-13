# -*- coding: utf-8 -*-
def Clamp(x, minVal, maxVal):
    pass


class Vector3(object):
    def __init__(self, *args):
        pass

    @staticmethod
    def One():
        pass

    @staticmethod
    def Up():
        pass

    @staticmethod
    def Down():
        pass

    @staticmethod
    def Left():
        pass

    @staticmethod
    def Right():
        pass

    @staticmethod
    def Forward():
        pass

    @staticmethod
    def Backward():
        pass

    def Normalized(self):
        pass

    def Length(self):
        pass

    def LengthSquared(self):
        pass

    def ToTuple(self):
        pass

    def Normalize(self):
        pass

    def Set(self, x=0.0, y=0.0, z=0.0):
        pass

    @staticmethod
    def Dot(a, b):
        pass

    @staticmethod
    def Cross(a, b):
        pass

    def __neg__(self):
        pass

    def __pos__(self):
        pass

    def __add__(self, other):
        pass

    def __radd__(self, other):
        pass

    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        pass

    def __rsub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __div__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __getitem__(self, i):
        pass

class Quaternion(object):
    def __init__(self, *args):
        pass

    @staticmethod
    def Euler(roll=0.0, pitch=0.0, yaw=0.0):
        pass

    @staticmethod
    def AngleAxis(angle=0.0, axis=Vector3.Up()):
        pass

    @staticmethod
    def Dot(a, b):
        pass

    @staticmethod
    def Cross(a, b):
        pass

    @staticmethod
    def Conjugate(q):
        pass

    @staticmethod
    def Inverse(q):
        pass

    def Length(self):
        pass

    def LengthSquared(self):
        pass

    def ToTuple(self):
        pass

    def Normalized(self):
        pass

    def Normalize(self):
        pass

    def EulerAngles(self):
        pass

    def __neg__(self):
        pass

    def __pos__(self):
        pass

    def __add__(self, other):
        pass

    def __radd__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __rsub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __div__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass
