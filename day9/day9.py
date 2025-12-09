

class Tile():
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def area(self, tile):
        return abs((tile.x - self.x +1 ) * (tile.y - self.y +1))
    def __str__(self):
        return f"{self.x},{self.y}"
class Grid():
    def __init__(self):
        self.tiles = []
    def add_tile(self, x,y):
        self.tiles.append(Tile(x,y))
    def parse(self, txt):
        x,y = txt.strip().split(",")
        self.add_tile(int(x),int(y))

with open("input.txt", "r") as f:
    file = f.readlines()
    grid = Grid()
    for line in file:
        grid.parse(line)
    largest = 0
    for t1 in grid.tiles:
        for t2 in grid.tiles:
            if t1 != t2:
                area = t1.area(t2)
                # print(area)
                if(area > largest):
                    # print('setting new', area)
                    largest = area 
                    # print(t1, t2)
    print(largest)
                
                
                
        