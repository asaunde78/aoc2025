

class Tile():
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def area(self, tile):
        return abs((tile.x - self.x +1 ) * (tile.y - self.y +1))
    def __str__(self):
        return f"<{self.x},{self.y}>"
    def __repr__(self):
        return (str(self))
class Grid():
    def __init__(self):
        self.tiles = {}
        
    def add_tile(self, x,y):
        if x in self.tiles:
            self.tiles[x].update({y:Tile(x,y)})
        else:
            self.tiles[x] = {y:Tile(x,y)}
    def get_x_neighbor(self, tile, offset):
        
        keys = sorted(self.tiles.keys())
        tile_ind = keys.index(tile.x)
        new_ind = tile_ind + offset 
        
        if new_ind >= 0 and new_ind < len(keys):
            new_x = keys[new_ind]
            # print(new_ind, keys)
            row = self.tiles[new_x]
            if tile.y in row:
                return row[tile.y]
            else:
                return self.get_x_neighbor(tile, offset  + (-1 if offset < 0 else 1) )
        else:
            return None
        
            
    def get_y_neighbor(self, tile, offset):
        
        row = self.tiles[tile.x]
        keys = sorted(row.keys())
        tile_ind = keys.index(tile.y)
        new_ind = tile_ind + offset 
        if new_ind >= 0 and new_ind < len(keys):
            new_y  = keys[new_ind]
            # print(new_ind, keys)
            return row[new_y]
        else:
            # print("new_ind",new_ind, keys)
            return None

    def get_neighbors(self, tile):
        north = grid.get_x_neighbor(tile, - 1)
        south = grid.get_x_neighbor(tile, + 1)
        east = grid.get_y_neighbor(tile, - 1)
        west = grid.get_y_neighbor(tile, + 1)
        return north,south,east,west
    
    def parse(self, txt):
        x,y = txt.strip().split(",")
        self.add_tile(int(x),int(y))

with open("test.txt", "r") as f:
    file = f.readlines()
    grid = Grid()
    for line in file:
        grid.parse(line)
    largest = 0
    for x, row in grid.tiles.items():
        for y, tile in row.items():
            n,s,e,w = grid.get_neighbors(tile)
            if(n and s):
                print("hi")
            if(e and w):
                print("hi", tile, e, w)
            
    print(largest)
                
                
                
        