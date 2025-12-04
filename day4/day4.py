

grid = []
total = 0
class Spot():
    def __init__(self, _type):
        self.type = _type
        self.neighbors = []
        self.count = -1
        
    def is_roll(self):
        return self.type == "@"
    def __str__(self):
        return self.get_type()
    def __repr__(self):
        return str(self)
    
    def get_type(self):
        return self.type
    def add_neighbor(self, n):
        self.neighbors.append(n)
    def check_neighbors(self):
        self.count = 0
        for neighbor in self.neighbors:
            self.count += neighbor.is_roll()
        return self.count
    def forklift_check(self):
        return self.check_neighbors() <= 3
    def process(self):
        
        if self.is_roll() and self.forklift_check(): 
            self.type = "x"
            print("after: ", self.type, )
            global total 
            total +=1 
            for neighbor in self.neighbors:
                if(neighbor.is_roll() and neighbor.forklift_check()):
                    neighbor.process()
        

with open("input.txt", "r") as f:
    file = f.readlines()
    for line in file:
        spots = map(lambda x: Spot(x), list(line.strip()))
        grid.append(list(spots))

for i, line in enumerate(grid):
    for j, item in enumerate(line):
        spot = grid[i][j]
        for x in range(-1,2):
            new_x = i + x  
            if new_x < 0 or new_x >= len(grid):
                continue 
            for y in range(-1,2):
                new_y = j + y 
                if new_y < 0 or new_y >= len(line):
                    continue
                if not(new_x == i and new_y == j) :
                    spot.add_neighbor(grid[new_x][new_y])
                    
print(grid)
for line in grid:
    for item in line:
        # print(item)
        item.process()
print(grid)
            # print("found", i , j, item.check_neighbors())


print(total)
        
        