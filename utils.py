import numpy as np

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point: (" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except:
            return False

    def __ne__(self,other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.x,self.y))

    def __contains__(self, pnt):
        return self.x == pnt.x and self.y == pnt.y

    def cross(self, other):
        return self.x*other.y-self.y*other.x
        
    def dot(self, other):
        return self.x*other.x+self.y*other.y

    def norm2(self):
        return self.dot(self)

    def between(self, other1, other2):
        v1 = other1-other2
        v2 = self - other2
        if np.isclose(v1.cross(v2), 0.0):
            v1dv1 = v1.dot(v1)
            v1dv2 = v1.dot(v2)
            if v1dv2 > 0 and v1dv2 < v1dv1:
                return True
        return False

class InvMat(object):
    def __init__(self,vec1,vec2):
        denom = vec1.x*vec2.y-vec1.y*vec2.x
        self.top = Point(vec2.y/denom,-vec2.x/denom)
        self.bottom = Point(-vec1.y/denom,vec1.x/denom)

    def __mul__(self,pt):
        return Point(self.top.dot(pt),self.bottom.dot(pt))

    def __str__(self):
        return 'Matrix:\n[[' + str(self.top.x) + ',' + str(self.top.y) + '],\n[' + str(self.bottom.x) + ',' + str(self.bottom.y) + ']]\n'
