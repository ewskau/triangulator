from utils import Point

class Vertex(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.edges = set([])
        self.triangles = set([])

    def push(self,pnt):
        return (set([]),set([])), (set([]),set([])), (set([]),set([]))
