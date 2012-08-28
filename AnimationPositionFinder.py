import copy
import sympy as sp

class AnimationPositions:
    
    nodeSymbols = {}
    inititated = False;
    idsToNodes = {}
    def __init__(self):
        self.initiated = False
    
    def find_head(self, diagram):
        for node in diagram.keys():
            if node.fixed:
                return node
        return diagram.keys()[0]
    
    def get_unvisited(self, diagram, visited):
        diagramCopy = copy.copy(diagram)
        for node in visited:
            del diagramCopy[node]
        return self.find_head(diagramCopy)
    
    def dfs(self, diagram, head, traj, varList, geom, origin):
        if not self.initiated:
            self.initiated = True
            for obj in geom:
                self.idsToNodes[obj.objId] = obj
            for node in diagram.keys():
                if node.get_type() == "Segment":
                    self.nodeSymbols[node.objId] = node.th
        for step in traj[::4]:
            angles = step[::2]
            angSymToVal = {}
            current = 0;
            for (var1, var2) in varList:
                if "th" in var1.name:
                    angSymToVal[var1] = angles[current]
                    current = current + 1
            for node in diagram.keys():
                if node.get_type() == "Segment":
                    node.th = angSymToVal[self.nodeSymbols[node.objId]]
            visited = []
            parents = {}
            next = []
            next.append(head)
            parents[head] = None
            while len(visited) < len(diagram.keys()):
                if len(next) == 0:
                    newHead = self.get_unvisited(diagram, visited)
                    next.append(newHead)
                    parents[newHead] = None
                    continue
                else:
                    current = next.pop()
                    visited.append(current)
                    drawable = self.idsToNodes[current.objId]
                    # Calculate qualities
                    if parents[current]:
                        if current.get_type() == "Segment" and parents[current].get_type() == "Segment" :
                            current.x0= parents[current].xf
                            current.y0= parents[current].yf
                            current.xf= current.x0 + current.L*sp.cos(current.th)
                            current.yf= current.y0 + current.L*sp.sin(current.th)
                            current.x = current.x0 + current.r*current.L*sp.cos(current.th)
                            current.y = current.y0 + current.r*current.L*sp.sin(current.th)
                            drawable.x0, drawable.y0, drawable.x1, drawable.y1 = current.x0 + origin[0], current.y0+ origin[1], current.xf+ origin[0], current.yf+ origin[1]
                            
                        elif current.get_type() == "Segment" and parents[current].get_type() == "Mass" :
                            current.x0= parents[current].x
                            current.y0= parents[current].y
                            current.xf= current.x0 + current.L*sp.cos(current.th)
                            current.yf= current.y0 + current.L*sp.sin(current.th)
                            current.x = current.x0 + current.r*current.L*sp.cos(current.th)
                            current.y = current.y0 + current.r*current.L*sp.sin(current.th)
                            drawable.x0, drawable.y0, drawable.x1, drawable.y1 = current.x0+ origin[0], current.y0+ origin[1], current.xf+ origin[0], current.yf+ origin[1]
                        else: #  current.get_type() == "Mass" and parents[current].get_type() == "Segment" :
                            current.x = parents[current].xf
                            current.y = parents[current].yf 
                            drawable.x, drawable.y = current.x+ origin[0], current.y+ origin[1]
                    else:
                        if current.get_type()=="Segment" and not current.fixed:
                            current.xf= current.x0 + current.L*sp.cos(current.th)
                            current.yf= current.y0 + current.L*sp.sin(current.th)
                            current.x = current.x0 + current.r*current.L*sp.cos(current.th)
                            current.y = current.y0 + current.r*current.L*sp.sin(current.th)
                            drawable.x0, drawable.y0, drawable.x1, drawable.y1 = current.x0+ origin[0], current.y0+ origin[1], current.xf+ origin[0], current.yf+ origin[1]
                        elif current.get_type() == "Mass":
                            drawable.x, drawable.y = current.x+ origin[0], current.y+ origin[1]
                    
                    for child in diagram[current]:
                        if not (child in visited or child in next):
                            next.append(child)
                            parents[child] = current
            yield geom