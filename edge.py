from vertex import Vertex
import triangle

class Edge(object):
    def __init__(self,a,b):
        self.vertices=set([a,b])
        self.triangles=set()
        self.add_self()

    def __str__(self):
        i = iter(self.vertices)
        return 'Edge:{\n\t' + str(next(i)) + '\n\t' + str(next(i)) + '\n}'

    def __repr__(self):
        return self.__str__()

    def __contains__(self, pnt):
        if pnt in self.vertices or pnt.between(*self.vertices):
            return True
        return False

    def add_self(self):
        for vert in self.vertices:
            vert.edges |= set([self])

    def push(self,pnt):
        v1,v2 = self.vertices
        t1,t2 = self.triangles
        
        #make triangle 1
        a1 = pnt
        b1 = v1
        c1 = t1.get(self)[0]
        ab1 = Edge(a1,b1)
        bc1 = t1.get(v2)[1]
        ac1 = Edge(a1,c1)
        abc1 = triangle.Triangle(a1,b1,c1,bc1,ac1,ab1)

        #make triangle 2
        a2 = pnt
        b2 = c1
        c2 = v2
        ab2 = ac1
        bc2 = t1.get(v1)[1]
        ac2 = Edge(a2,c2)
        abc2 = triangle.Triangle(a2,b2,c2,bc2,ac2,ab2)

        #make triangle 3
        a3 = pnt
        b3 = c2
        c3 = t2.get(self)[0]
        ab3 = ac2
        bc3 = t2.get(v1)[1]
        ac3 = Edge(a3,c3)
        abc3 = triangle.Triangle(a3,b3,c3,bc3,ac3,ab3)

        #make triangle 4
        a4 = pnt
        b4 = c3
        c4 = b1
        ab4 = ac3
        bc4 = t2.get(v2)[1]
        ac4 = ab1
        abc4 = triangle.Triangle(a4,b4,c4,bc4,ac4,ab4)

        #for b1, remove t1 t2, remove self
        b1.edges -= set([self])
        b1.triangles -= set([t1,t2])
        #for b2, remove t1
        b2.triangles -= set([t1])
        #for b3, remove t1 t2, remove self
        b3.edges -= set([self])
        b3.triangles -= set([t1,t2])
        #for b4, remove t2
        b4.triangles -= set([t2])

        #for bc1, remove t1
        bc1.triangles -= set([t1])
        #for bc2, remove t1
        bc2.triangles -= set([t1])
        #for bc3, remove t2
        bc3.triangles -= set([t2])
        #for bc4, remove t2
        bc4.triangles -= set([t2])

        #for abc1, set neighboring triangles
        abc1.data[0][2] = t1.get(v2)[2]
        abc1.data[1][2] = abc2
        abc1.data[2][2] = abc4
        if abc1.data[0][2] is not None:
            abc1.data[0][2].replace(t1,abc1)

        #for abc2, set neighboring triangles
        abc2.data[0][2] = t1.get(v1)[2]
        abc2.data[1][2] = abc3
        abc2.data[2][2] = abc1
        if abc2.data[0][2] is not None:
            abc2.data[0][2].replace(t1,abc2)

        #for abc3, set neighboring triangles
        abc3.data[0][2] = t2.get(v1)[2]
        abc3.data[1][2] = abc4
        abc3.data[2][2] = abc2
        if abc3.data[0][2] is not None:
            abc3.data[0][2].replace(t2,abc3)

        #for abc4, set neighboring triangles
        abc4.data[0][2] = t2.get(v2)[2]
        abc4.data[1][2] = abc1
        abc4.data[2][2] = abc3
        if abc4.data[0][2] is not None:
            abc4.data[0][2].replace(t2,abc4)


        return (set([pnt]),set([])), (set([ab1,ab2,ab3,ab4]),set([self])), (set([abc1,abc2,abc3,abc4]),set([t1,t2]))
        
