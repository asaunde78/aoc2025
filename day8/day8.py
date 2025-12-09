from functools import reduce
import json
import math 

point_counter = 0
class Point():
    def __init__(self, x,y,z):
        global point_counter 
        
        self.id = point_counter 
        point_counter += 1
        self.x = x
        self.y = y
        self.z = z
    def get_data(self):
        return [self.x,self.y,self.z]
    # def distance(self, point):
    def dist_squared(self, point):
        dist = 0 
        for val in self.difference(point):
            dist += val * val
        return dist
    def difference(self, point):
        output = []
        data = self.get_data()
        for i,val in enumerate(point.get_data()):
            output.append(val - data[i])
        return output
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f"<{self.x},{self.y},{self.z}>"

def parse_point(txt):
    x,y,z = txt.strip().split(",")
    return Point(int(x),int(y),int(z))
class Circuit():
    def __init__(self, start):
        self.nodes = [start]
    def circuit_distance(self, circuit):
        dist = -1
        best_other_node = None
        best_local_node = None
        for point1 in self.nodes:
            for point2 in circuit.nodes:
                
                distance = point1.dist_squared(point2)

                if(distance < dist or dist == -1):
                    dist = distance 
                    best_local_node = point1
                    best_other_node = point2 
        return dist, best_local_node, best_other_node
    def merge_circuit(self, circuit):
        for node in circuit.nodes:
            self.nodes.append(node)

class Distance():
    def __init__(self, dist_dict):
        self.dist_dict = dist_dict
        self.sorted_distances = sorted(dist_dict.items(), key=lambda x: x[1], )
    def nth_distance(self, n):
        return self.sorted_distances[n]
    def get_distance(self, n):
        return self.dist_dict.get(n)
    
        
class Distances():
    def __init__(self, points):
        self.distances = {}
        for p1 in points:
            output = {}
            for p2 in points: 
                output[p2] = p1.dist_squared(p2)
                
            self.distances[p1] = Distance(output)
    def node_n_dist(self, n, node):
        return self.distances[node].nth_distance(n)
    def get_dist(self, n1, n2):
        return self.distances[n1].get_distance(n2)
                

# with open("test.txt", "r") as f:
#     lines = f.readlines()
#     circuits = []
#     points = []
#     for line in lines:
#         circuits.append(Circuit(parse_point(line)))
#         points.append(parse_point(line))
#     distances = Distances(points)
    
#     for point in points:
#         print(distances.node_n_dist(1, point))
    
    

    # closest_distance = -1 
    # for x in circuits:
    #     for y in circuits:
    #         if x != y:
    #             distance,n1, n2 = x.circuit_distance(y)
    #             if(distance < closest_distance or closest_distance == -1):
    #                 closest_distance = distance
    #                 print(distance, n1, n2)
class Circuit():
    def __init__(self):
        self.nodes = set()
    def has_node(self, node):
        return node in self.nodes 
    def add_node(self, node):
        self.nodes.add(node)
    def get_count(self):
        return len(self.nodes)
    def get_nodes(self):
        return self.nodes
    def merge(self, circuit):
        self.nodes.update(circuit.nodes)
        
def new_circuit(c1,c2):
    temp = c1.get_nodes()
    temp.update(c2.get_nodes())
    c = Circuit()
    for node in temp:
        c.add_node(node)
    return c
with open("input.txt", "r") as f:
    lines = f.readlines()
    distances = []
    points = []
    for line in lines:
        points.append(parse_point(line))
    d = Distances(points)
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            if x != y and i <= j:
                distance = d.get_dist(x,y)
                distances.append((distance, x,y,))
    distances = sorted(distances, key=lambda x: x[0])
    
    circuit_map = {}
    for point in points:
        c = Circuit()
        c.add_node(point)
        circuit_map[point] = c
    
    
    for d,n1,n2 in distances[:1000]: 
        print(d,n1,n2,)
        
        if circuit_map[n1].get_nodes() != circuit_map[n2].get_nodes():
            # print(n1,n2,circuit_map[n1],circuit_map[n2])
            # print("merging n1 and n2", n1, n2)
            # print("\tnodes to merge", circuit_map[n1].get_nodes(), circuit_map[n2].get_nodes())
            circuit_map[n1].merge(circuit_map[n2])
            del circuit_map[n2]
            
            
            for node in circuit_map[n1].get_nodes():
                circuit_map[node] = circuit_map[n1]
            # new = new_circuit(circuit_map[n1], circuit_map[n2])
            # circuit_map[n1] = new
            # circuit_map[n2] = new
            
            
        
        # found = False 
        # for circuit in circuit_map.values():
        #     if circuit.has_node(n1):
        #         print("adding node")
        #         found = True
        #         circuit.add_node(n2)
        #         break 
        #     if circuit.has_node(n2):
        #         print("adding node")
        #         circuit.add_node(n1)
        #         found = True
        #         break
        #     print("not in any circuits")
        # if found:
        #     continue
        # if n1 in circuit_map and n2 in circuit_map:
        #     continue 
        # if n1 in circuit_map and n2 not in circuit_map:
        #     circuit_map[n1].add_node(n2)
        #     print("\tAdding new node to Circuit", n2)
        #     continue
        # if n2 in circuit_map and n1 not in circuit_map:
        #     circuit_map[n2].add_node(n1)
        #     print("\tAdding new node to Circuit", n1)
        #     continue
        # if n1 not in circuit_map and n2 not in circuit_map:
        #     print("\tAdding to Circuit Map:",n1,n2)
        #     new_circ = Circuit()
        #     new_circ.add_node(n1)
        #     new_circ.add_node(n2)
        #     circuit_map[n1] = new_circ 
        #     circuit_map[n2] = new_circ
        #     continue
        # print("what", d,n1,n2)
        
    # for key,val in circuit_map.items():
    #     print(key, val.get_nodes(), val.get_count())
    print()
    total = 1
    for circuit in sorted(set(circuit_map.values()), key=lambda x: x.get_count(), reverse=True)[:3]:
        total *= circuit.get_count()
        print(circuit, circuit.get_count(), circuit.get_nodes())
    print("--------\n Total: ", total)
    