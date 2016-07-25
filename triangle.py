from utils import *
import edge

class Triangle(object):
    def __init__(self, a,b,c,bc,ac,ab,A=None,B=None,C=None):
        self.data = [[a,bc,A],[b,ac,B],[c,ab,C]]
        for i in [0,1,2]:
            for j in [0,1]:
                self.data[i][j].triangles |= set([self])
        self.setup()

    def setup(self):
        self.offset = self.data[0][0]

        bma = self.data[1][0] - self.data[0][0]
        bma2 = bma.norm2()
        cma = self.data[2][0] - self.data[0][0]
        cma2 = cma.norm2()
        inv_denom = .5/bma.cross(cma)
        
        self.change_basis_matrix = InvMat(bma,cma)
        
        self.center = Point((cma.y*bma2-bma.y*cma2)*inv_denom,(bma.x*cma2-cma.x*bma2)*inv_denom) + self.offset
        self.r2 = (self.offset-self.center).norm2()

    def delaunayize(self):
        for i in range(3):
            triangle = self.data[i][2]
            if triangle is not None:
                if self.should_flip(triangle):
                    self.flip(triangle)
                    self.delaunayize()
                    triangle.delaunayize()
        
    def should_flip(self,other):
        return (self.get(other)[0] - other.center).norm2() < other.r2
        
    def flip(self,other):
        e = self.get(other)[1]
        v1,v2 = e.vertices
        e11, t11 = self.get(v2)[1:]
        e21, t21 = self.get(v1)[1:]
        e12, t12 = other.get(v2)[1:]
        e22, t22 = other.get(v1)[1:]
        nv1 = self.get(other)[0]
        nv2 = other.get(self)[0]
        e.vertices = set([nv1,nv2])
        self.replace(v1,nv2)
        self.replace(e,e22)
        self.replace(e11,e)
        self.replace(other,t22)
        self.replace(t11,other)
        
        other.replace(v2,nv1)
        other.replace(e,e11)
        other.replace(e22,e)
        other.replace(self,t11)
        other.replace(t22,self)

        if t22 is not None:
            t22.replace(other,self)
        if t11 is not None:
            t11.replace(self,other)

        e22.triangles -= set([other])
        e22.triangles |= set([self])

        e11.triangles -= set([self])
        e11.triangles |= set([other])

        nv1.triangles |= set([other])
        v2.triangles -= set([other])
        nv2.triangles |= set([self])
        v1.triangles -= set([self])
        self.setup()
        other.setup()
        
        

    def change_basis(self,pnt):
        return self.change_basis_matrix*(pnt-self.offset)

    def find(self, pnt):
        cb = self.change_basis(pnt)
        if cb.x < 0.0:
            if self.data[1][2] is not None:
                return self.data[1][2].find(pnt)
        if cb.y < 0.0:
            if self.data[2][2] is not None:
                return self.data[2][2].find(pnt)
        if cb.x + cb.y > 1.0:
            if self.data[0][2] is not None:
                return self.data[0][2].find(pnt)
        if 0.0 < cb.x < 1.0 and 0.0 < cb.y < 1.0 and cb.x+cb.y < 1.0:
            return self
        for edge in self.edges:
            if pnt in  edge:
                return edge
        for vert in self.vertices:
            if pnt in vert:
                return vert
        return self
        

    @property
    def vertices(self):
        return set([self.data[i][0] for i in range(3)])

    @property
    def edges(self):
        return set([self.data[i][1] for i in range(3)])

    @property
    def triangles(self):
        return set([selt.data[i][2] for i in range(3)])

    def __contains__(self,pnt):
        if pnt in self.vertices:
            return True
        if pnt in self.edges:
            return True
        bc = self.change_basis(pnt)
        if 0 < bc.x < 1 and 0 < bc.y < 1 and bc.x+bc.y < 1:
            return True
        return False

    def get(self,obj):
        for sublist in self.data:
            if obj in sublist:
                return sublist
        return None

    def __str__(self):
        return "triangle:{\n\t" + str(self.data[0][0])+'\n\t' + str(self.data[1][0]) + '\n\t' + str(self.data[2][0]) + '\n}\n'

    def __repr__(self):
        return self.__str__()
    
    def replace(self,thing1, thing2):
        for i in range(3):
            for j in range(3):
                if self.data[i][j] == thing1:
                    self.data[i][j] = thing2
    
    def push(self,pnt):
        #make triangle 1
        a1 = pnt
        b1 = self.data[0][0]
        c1 = self.data[1][0]
        ab1 = edge.Edge(a1, b1)
        bc1 = self.data[2][1]
        ac1 = edge.Edge(a1,c1)
        abc1 = Triangle(a1,b1,c1,bc1,ac1,ab1)

        #make triangle 2
        a2 = pnt
        b2 = c1
        c2 = self.data[2][0]
        ab2 = ac1
        bc2 = self.data[0][1]
        ac2 = edge.Edge(a2,c2)
        abc2 = Triangle(a2,b2,c2,bc2,ac2,ab2)

        #make triangle 3
        a3 = pnt
        b3 = c2
        c3 = b1
        ab3 = ac2
        bc3 = self.data[1][1]
        ac3 = ab1
        abc3 = Triangle(a3,b3,c3,bc3,ac3,ab3)

        #for b1 remove self
        b1.triangles -= set([self])
        #for b2 remove self
        b2.triangles -= set([self])
        #for b3 remove self
        b3.triangles -= set([self])

        #remove self from bc1
        bc1.triangles -= set([self])
        #remove self from bc2
        bc2.triangles -= set([self])
        #remove self from bc3
        bc3.triangles -= set([self])

        #for abc1, set neighboring triangles
        abc1.data[0][2] = self.data[2][2]
        abc1.data[1][2] = abc2
        abc1.data[2][2] = abc3
        if abc1.data[0][2] is not None:
            abc1.data[0][2].replace(self, abc1)

        #for abc2, set neighboring triangles
        abc2.data[0][2] = self.data[0][2]
        abc2.data[1][2] = abc3
        abc2.data[2][2] = abc1
        if abc2.data[0][2] is not None:
            abc2.data[0][2].replace(self, abc2)

        #for abc3, set neighboring triangles
        abc3.data[0][2] = self.data[1][2]
        abc3.data[1][2] = abc1
        abc3.data[2][2] = abc2
        if abc3.data[0][2] is not None:
            abc3.data[0][2].replace(self, abc3)

        return (set([pnt]),set([])), (set([ab1,ab2,ab3]),set([])), (set([abc1,abc2,abc3]),set([self]))
        
