from utils import *
import vertex
import edge
import triangle

class Triangulation(object):
    def __init__(self,A,B,C):
        
        # make 3 vertices
        a = vertex.Vertex(*A)
        b = vertex.Vertex(*B)
        c = vertex.Vertex(*C)

        # make the three edges
        ab = edge.Edge(a,b)
        bc = edge.Edge(b,c)
        ac = edge.Edge(c,a)

        # make one triangle
        abc = triangle.Triangle(a,b,c,bc,ac,ab)

        self.triangles = set([abc])
        self.edges = set([ab,bc,ac])
        self.vertices = set([a,b,c])

    def addremove(self,arg):
        vertices, edges, triangles = arg
        self.vertices |= vertices[0]
        self.vertices -= vertices[1]
        self.edges |= edges[0]
        self.edges -= edges[1]
        self.triangles |= triangles[0]
        self.triangles -= triangles[1]

    
    def push(self,p):
        pnt = vertex.Vertex(p[0],p[1])
        obj = next(iter(self.triangles)).find(pnt)
        if obj is not None:
            vertices,edges,triangles = obj.push(pnt)
            self.addremove((vertices,edges,triangles))


class Delaunay(Triangulation):
    def __init__(self,A,B,C):
        Triangulation.__init__(self,A,B,C)

    def push(self,p):
        pnt = vertex.Vertex(p[0],p[1])
        obj = next(iter(self.triangles)).find(pnt)
        if obj is not None:
            vertices,edges,triangles = obj.push(pnt)
            self.addremove((vertices,edges,triangles))
            for triangle in triangles[0]:
                triangle.delaunayize()



if __name__ == '__main__':
#def main():
    import matplotlib.pyplot as plt
    import numpy as np
    import timeit
    a,b,c=(-3.0,-1.0),(3.0,-1.0),(0.0,3.0)
    #T = Triangulation(a,b,c)
    times = []
    #ns = [int(x) for x in np.linspace(0,10000,num=100)]
    ns = [100,10000]
    for n in ns:
        tstart = timeit.default_timer()        
        D = Delaunay(a,b,c)
        for i in range(n):
            D.push((np.random.rand(1)[0],np.random.rand(1)[0]))
        tstop = timeit.default_timer()
        times.append(tstop-tstart)
    fig = plt.figure()
    #plt.plot(ns,times)
    for edge in D.edges:
       v1, v2 = edge.vertices
       plt.plot((v1.x,v2.x),(v1.y,v2.y),'k')
    ax = plt.gca()
    for triangle in D.triangles:
       ax.add_artist(plt.Circle((triangle.center.x,triangle.center.y),np.sqrt(triangle.r2),alpha=.1))
    ax.set_xlim([.25,.75])
    ax.set_ylim([.25,.75])
    fig.show()

    
