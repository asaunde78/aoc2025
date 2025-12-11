
class Tile():
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.prev = None 
        self.next = None
    def area(self, tile):
        return abs((tile.x - self.x +1 ) * (tile.y - self.y +1))
    def other_corners(self, tile):
        if(self.x == tile.x or self.y == tile.y):
            return None 
        return [Tile(self.x, tile.y), Tile(tile.x, self.y)]
    def set_prev(self, tile):
        self.prev = tile
    def set_next(self, tile):
        self.next = tile 
    
    def __str__(self):
        return f"<{self.x},{self.y}>"
    def __repr__(self):
        return (str(self))
    def is_related(self, tile):
        return self.next == tile or self.prev == tile
class Grid():
    def __init__(self):
        self.tile_list = []
        self.tiles = {}
        self.enclosed = {}
        self.largest_x = 0
        self.largest_y = 0
    def has_tile(self, tile):
        if tile.x not in self.tiles:
            return False 
        if tile.y not in self.tiles[tile.x]:
            return False
        return True
    def get_tile(self, tile):
        if(self.has_tile(tile)):
            return self.tiles[tile.x][tile.y]
        return tile
    def add_tile(self, x,y):
        tile_out = Tile(x,y)
        if x > self.largest_x: 
            self.largest_x = x 
        if y > self.largest_y: 
            self.largest_y = y 
        self.tile_list.append(tile_out)
        if x in self.tiles:
            self.tiles[x].update({y:tile_out})
        else:
            self.tiles[x] = {y:tile_out}
        return tile_out 
    def tile_between(self, tile1, tile2):
        xs = [tile1.x, tile2.x]
        min_x = min(xs)
        max_x = max(xs)
        
        
        between_x = self.keys_inbetween(self.tiles, min_x, max_x)
        if (len(between_x) == 0):
            return []
        
        ys = [tile1.y, tile2.y]
        min_y = min(ys)
        max_y = max(ys)
        output = []
        for i in between_x:
            between_y = self.keys_inbetween(self.tiles[i], min_y, max_y)
            if( len(between_y) == 0):
                continue
            else:
                for y in between_y:
                    output.append(self.tiles[i][y])
                # return True
        # print("nothing found between", tile1, tile2)
        return output
    def tile_enclosed(self, tile):
        if tile.x in self.enclosed and tile.y in self.enclosed[tile.x]:
            return self.enclosed[tile.x][tile.y]
            
        lt = sorted(self.filter_keys(self.tiles, lambda x: x <= tile.x), reverse=True)
        
        if (len(lt) == 0):
            return False 
        # print(lt)
        
        # curl = {"t1->t2":0,"t2->t1":0}
        for x in lt:
            # print(x)
            row = self.tiles[x]
            keys = sorted(row.keys())
            target_y = tile.y 
            frame = list(map(lambda x: x - target_y, keys))
            
            mindex = frame.index(min(frame))
            nextdex = mindex+1
            y1 = keys[mindex]
            y2 = None 
            if nextdex < len(keys):
                y2 = keys[nextdex]
            
            if target_y > y2 or target_y < y1:
                continue
            if x == tile.x:
                if (tile.x in self.enclosed):
                    self.enclosed[tile.x][tile.y] = True 
                else:
                    self.enclosed[tile.x] = {tile.y: True}
                return True
            t1 = row[y1] 
            t2 = row[y2]
            if not ( t2 == t1.next or t1 == t2.next ):
                print(f"VERY BAD: {t1} {t1.next} {t1.prev} {t2} {t2.next} {t2.prev}")
            
            if t2 == t1.next:
                return True
                # curl["t1->t2"] += 1
            if t1==t2.next:
                return False
                # curl["t1->t2"] += 1
                
        # print(curl)
            # print(x,tile.x, keys, mindex, tile)
            
            
        
    def keys_inbetween(self, _dict, _min, _max):
        return list(filter(lambda x: x > _min and x < _max, _dict.keys()))
    def filter_keys(self, _dict, _filter):
        return list(filter(_filter, _dict))
    
    def parse(self, txt):
        x,y = txt.strip().split(",")
        return self.add_tile(int(x),int(y))
        

with open("input.txt", "r") as f:
    file = f.readlines()
    grid = Grid()
    
    before = grid.parse(file[0])
    start = before
    for line in file[1:]:
        
        ti = grid.parse(line)
        before.set_prev(ti)
        ti.set_next(before)
        before = ti 
    start.set_next(ti)
    ti.set_prev(start)
    print("finished parsing")
        
    largest = 0 
    
    # target = grid.tile_list[2]
    # print("Target:",target)
    # grid.tile_enclosed(target)
    # print(grid.largest_x, grid.largest_y)
    # output = ""
    # for x in range(grid.largest_x+2):
    #     for y in range(grid.largest_y+2)[::-1]:
    #         tenc = grid.tile_enclosed(Tile(x,y))
    #         gtile = grid.has_tile(Tile(x,y))
    #         if(gtile):
    #             output+= "X"
    #         elif(tenc):
    #             output+= "#"
    #         else:
    #             output += "."
    #     output += "\n" 
    # print(output)
    print(grid.largest_x, grid.largest_y)
    
    print("created image")
    for t1 in grid.tile_list:
        for t2 in grid.tile_list:
            if t1 == t2:
                continue
            img.putpixel((t1.x, t1.y), (0,0,0))
            print("working?")
            between = grid.tile_between(t1,t2)
            
            if between != []:
                continue  
            # print(between)
            corners = t1.other_corners(t2)
            if not corners:
                continue 
            good = True
            for corner in corners: 
                
                select_tile = grid.get_tile(corner)
                if not grid.tile_enclosed(select_tile):
                    good = False 
                    break

            
            if not good:
                continue 
            area =  t1.area(t2)
            if area > largest:
                print("Setting Largest", area, t1,t2)
                
                largest = area
    
    print("done", largest)
    