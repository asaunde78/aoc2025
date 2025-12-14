from  PIL import Image

class Tile():
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.prev = None 
        self.next = None
    def area(self, tile):
        return  (abs(tile.x - self.x) + 1 ) * (abs(tile.y - self.y) + 1 )
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
        self.reversed_tiles = {}
        self.enclosed = {}
        self.largest_x = 0
        self.largest_y = 0
        self.outlines = {}
        self.curl = 0
    def get_curl(self, tile1, tile2):
        if tile1.x == tile2.x:
            return tile1.y > tile2.y
        return tile1.x < tile2.x 
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
        if y in self.reversed_tiles:
            self.reversed_tiles[y].update({x:tile_out})
        else:
            self.reversed_tiles[y] = {x:tile_out}
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
    def set_curl(self, val):
        self.curl = val
    def is_colinear(self, tile1, tile2):
        return (tile1.x == tile2.x or tile1.y == tile2.y)
    def curl_between(self, _dict, _min, _max, curl_val, tile1, tile2):
        between_slices = sorted(self.filter_keys(_dict.keys(), lambda i: i < _max and i > _min), reverse=True)
        
        # if len(between_slices) == 0:
        #     if(self.has_tile(tile1) and self.has_tile(tile2)):
        #         return True
        #     return False 
        pen_loops = []
        for slice_coord in between_slices:
            above = {}
            below = {}
            zeros = {}
            for coord, tile in _dict[slice_coord].items():
                # print(slice_coord, coord, tile, curl_val)
                if coord < curl_val:
                    below.update({coord:tile})
                if coord > curl_val:
                    above.update({coord:tile})
                if coord == curl_val:
                    zeros.update({coord:tile})
            # print("AB", slice_coord, above, below)
            
            
            for coord, b in below.items():
                # print("Coordinate and keys: ", coord, above.keys())
                
                if (b.next  in above.values()):
                    
                    # print("FOUND FOUND FOUND", b, b.prev)
                    pen_loops.append([b, b.next])
                if (b.prev  in above.values()):
                    
                    # print("FOUND FOUND FOUND", b, b.prev)
                    pen_loops.append([b.prev, b])
            for coord, zero in zeros.items():
                if zero.prev in below.values():
                    pen_loops.append([zero, zero.prev ]) 
                if zero.next in below.values():
                    pen_loops.append([zero, zero.next]) 
                if zero.prev in above.values():
                    pen_loops.append([zero, zero.prev]) 
                if zero.next in above.values():
                    pen_loops.append([zero, zero.next]) 
            # print("ABOVE SO BELOW", above, below)
        # if len(pen_loops) == 0:
        #     # print(" NO LOOPS")
        #     if(self.has_tile(tile1) and self.has_tile(tile2)):
        #         return True
        #     return False
        # print("PEN LOOPS", [[self.get_curl(t1,t2), t1, t2] for t1,t2 in pen_loops])
        return pen_loops
        

            
            
    def line_enclosed(self, tile1, tile2):
        print("---------------------Starting Line Check for: ", tile1, tile2,)
        if(not self.is_colinear(tile1, tile2)):
            print("this is not a straight line")
            return False
        if(not self.tile_enclosed(tile1)):
            print("Not enclosed: ", tile1)
            return False
        if(not self.tile_enclosed(tile2)):
            print("Not enclosed: ", tile2)
            return False
        
        if( tile1.x == tile2.x):
            min_y, max_y = sorted([tile1.y, tile2.y])
            loops = self.curl_between(self.reversed_tiles,min_y, max_y,tile1.x, tile1, tile2)
           
            if len(loops) == 0:
                return self.tile_enclosed(Tile(tile1.x, (tile1.y + tile2.y) // 2))
            for t1, t2 in loops:
                test_tile1 = Tile(tile1.x, t2.y + 1) 
                test_tile2 = Tile(tile1.x, t2.y - 1)
                
                if not self.tile_enclosed(test_tile1):
                    return False 
                if not self.tile_enclosed(test_tile2):
                    return False 
            return True 
        else:
            min_x, max_x = sorted([tile1.x, tile2.x])
            loops = self.curl_between(self.tiles,min_x, max_x,tile1.y, tile1, tile2)
            if len(loops) == 0:
                return self.tile_enclosed(Tile((tile1.x + tile2.x) // 2, tile2.y))
            for t1, t2 in loops:
               
                test_tile1 = Tile(t1.x + 1, tile1.y) 
                test_tile2 = Tile(t1.x - 1, tile2.y)
                
                if not self.tile_enclosed(test_tile1):
                    return False 
                if not self.tile_enclosed(test_tile2):
                    return False 
                
            return True 
    
    def tile_enclosed(self, _tile):
        tile = self.get_tile(_tile)
        if tile.x in self.enclosed and tile.y in self.enclosed[tile.x]:
            # print("tile found:" , tile)
            return self.enclosed[tile.x][tile.y]
            
        lt = sorted(self.filter_keys(self.tiles, lambda x: x <= tile.x), reverse=True)
        
        if (len(lt) == 0):
            return False 
        # print(lt)
        
        curl = {"t1->t2":0,"t2->t1":0}
        # print("--------Starting Tile: ", tile)
        prev_tiles = None
        for x in lt:
            # print(x)
            row = self.tiles[x]
            keys = sorted(row.keys())
            target_y = tile.y 
            frame = list(map(lambda y: abs(y - target_y), keys))
            # print(tile, "keys: ", keys, "frame: ", frame, "x: ", x)
            
            mindex = frame.index(min(frame))
            closest = keys[mindex]
            closest_tile = row[closest]
            keys.remove(closest)
            left = keys
            
            opt_next =  closest_tile.next.y 
            
            lower_y,upper_y = sorted([closest_tile.y,closest_tile.next.y])
            
            # if closest_tile.x == tile.x and target_y <= upper_y or target_y >= lower_y:
            #     return True
            opt_prev = closest_tile.prev.y
            # print(closest, opt_prev, opt_next, keys)
            
            t1 = closest_tile
            # print(opt_next in left and opt_prev in left)
            if opt_next in left:
                t2 = t1.next
            elif opt_prev in left:
                temp = t1 
                t1 = t1.prev
                t2 = temp 
            else:
                print(f"BROKEN: {opt_prev} {opt_next} {left}")
                return None, None, None
            
            lower_y,upper_y = sorted([t1.y,t2.y])
            if target_y > upper_y or target_y < lower_y:
                continue
            # print(t1, t2)
            if t1.y == tile.y:
                # print("first", tile.x, t1.x, t1.y, tile.y, t1.prev.y)
                lower_x,upper_x = sorted([t1.x,t1.prev.x])
                # print(lower_x, tile.x, upper_x)
                if tile.x < upper_x and tile.x > lower_x:
                    return True
            if t2.y == tile.y:
                # print("second", tile.x, t2.x, tile.y, t2.next.x)
                lower_x,upper_x = sorted([t2.x,t2.next.x])
                # print(lower_x, tile.x, upper_x)
                if tile.x < upper_x and tile.x > lower_x:
                    return True
                
            
            # print(f"X:{x} {t1}{t2} " )
            # print(f"tile:{tile} x:{x}, y1:{y1}, y2:{y2}, keys:{keys}")
            
            if x == tile.x:
                # print("escaping early", x, tile)
                if (tile.x in self.enclosed):
                    self.enclosed[tile.x][tile.y] = True 
                else:
                    self.enclosed[tile.x] = {tile.y: True}
                return True
            
            if not ( t2 == t1.next or t1 == t2.next ):
                print(f"VERY BAD: {t1} {t1.next} {t1.prev} {t2} {t2.next} {t2.prev}")
            # print(f"creating curl {t1}, {t2}, {t1.y > t2.y}")
            found_prev = False
            if(t1.x == t2.x):
                c = t1.y > t2.y
            else:
                c = t1.x < t2.x
            if(prev_tiles and c == prev_tiles[2]):
                # print("CHECKING", t1, t2, t1.prev, t2.prev, prev_tiles)
                
                # print("CURL: ", c)

                if(t1.prev in prev_tiles or t2.prev in prev_tiles):
                    # print("found tile hehe")
                    found_prev = True
                if(t1.next in prev_tiles or t2.next in prev_tiles):
                    # print("found tile hehe")
                    found_prev = True
            prev_tiles = (t1, t2, c)
            if t1.y > t2.y:
                # print(f"curl direction {t1}, {t2}")
                if not found_prev:
                    curl["t1->t2"] += 1
                # return True
            else:
                # print(f"curl direction {t2}, {t1}")
                if not found_prev:
                    curl["t2->t1"] += 1
                # return False
        c1 = curl["t1->t2"]
        c2 = curl["t2->t1"]
        
        # print("final check", tile, c1, c2, (c1-c2), )
        test = (c1-c2) if  self.curl else (c2-c1)

        cond = test > 0 
        if ( cond ):
            if (tile.x in self.enclosed):
                self.enclosed[tile.x][tile.y] = True 
            else:
                self.enclosed[tile.x] = {tile.y: True}
            return True
        
        
        if (tile.x in self.enclosed):
            self.enclosed[tile.x][tile.y] = False 
        else:
            self.enclosed[tile.x] = {tile.y: False}
        return False
        
            # print(x,tile.x, keys, mindex, tile)
            
    def check_outline(self, tile1, tile2):
        # tileset = frozenset([tile1,tile2])
        # if(tileset in self.outlines):
        #     return self.outlines[tileset]
        # min_x, max_x = sorted((tile1.x, tile2.x)) 
        # min_y, max_y = sorted((tile1.y, tile2.y)) 
        if(self.is_colinear(tile1, tile2)):
            return self.line_enclosed(tile1, tile2)
        # print(tile1.other_corners(tile2), tile2.other_corners(tile1))
        for corner in tile1.other_corners(tile2):
            if not self.line_enclosed(tile1, corner):
                return False

        for corner in tile2.other_corners(tile1):
            if not self.line_enclosed(tile2, corner):
                return False
        return True
        
        
    def keys_inbetween(self, _dict, _min, _max):
        return list(filter(lambda x: x > _min and x < _max, _dict.keys()))
    def filter_keys(self, _dict, _filter):
        return list(filter(_filter, _dict))
    
    def parse(self, txt):
        x,y = txt.strip().split(",")
        return self.add_tile(int(x),int(y))

def setup(input_file):
    grid = Grid()
    with open(input_file, "r") as f:
        file = f.readlines()
        
        
        before = grid.parse(file[0])
        start = before
        for line in file[1:]:
            
            ti = grid.parse(line)
            before.set_prev(ti)
            ti.set_next(before)
            before = ti 
        start.set_next(ti)
        ti.set_prev(start)
        
        if(start.x == ti.x):
            grid.set_curl(start.y > ti.y)
        else:
            grid.set_curl(start.x < ti.x)
        print(grid.largest_x, grid.largest_y)
        print("finished parsing", grid.curl)
    return grid 
            
        
def draw(grid, path):
    
    largest = 0 
    img = Image.new("RGB", (grid.largest_x+1, grid.largest_y+1), 'white')
    print("created image")
    # target = grid.tile_list[2]
    # print("Target:",target)
    # grid.tile_enclosed(target)
    print(grid.largest_x, grid.largest_y)
    # output = ""
    for x in range(grid.largest_x+1):
        for y in range(grid.largest_y+1)[::-1]:
            tenc = grid.tile_enclosed(Tile(x,y))
            gtile = grid.has_tile(Tile(x,y))
            color = (255,255,255)
            # print("enclosed check", Tile(x,y), tenc)
            if(tenc):
                color = (0,255,0)
            if(gtile):
                color = (255,0,0)
            img.putpixel( (x,y), color)
            
    # test = Tile(5,2)
    # img.putpixel((test.x, test.y), (0,0,255))
    # grid.tile_enclosed(test)
    img.save(path)
    return img
    
        
def main(input_file, drawing = ""):
    largest = 0 
    grid = setup(input_file)
    img = None 
    if drawing != "":
        img = draw(grid, drawing)
    largest_pair = None
    for ind, t1 in enumerate(grid.tile_list):
        for t2 in grid.tile_list:
            if t1 == t2:
                continue
            
            area =  t1.area(t2)
            if area < largest:
                continue
            print("\n----------Checking Outline,",t1,t2)
            outline = grid.check_outline(t1,t2)
            print("Outline results: ", outline, "Results:", area, t1,t2, ind/len(grid.tile_list))
            if outline:
                print("Setting Largest", area, t1,t2, grid.tile_between(t1,t2))
                
                largest = area
                largest_pair = (t1, t2)
    if img:
        for point in largest_pair:
            img.putpixel( (point.x,point.y), (0,0,255))
        img.save(drawing)
    print("done", largest, largest_pair)

# main("test.txt", drawing="p1.png") 

# main("advent_test.txt", drawing="p2.png") 

#checking outline <97819,50252> <97819,49040> 0.9979838709677419
#done 1537423615 (<94851,50236>, <5605,67462>)

# draw(setup("new_test.txt"),"d9.png")
main("input.txt")#, drawing="videos/d9.png")
    