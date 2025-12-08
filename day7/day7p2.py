class Component():
    def __init__(self, _type, placement):
        self.type = _type
        self.placement = placement
        
        self.options = None
        self.left = None
        self.right = None
    def __str__(self):
        return f"<{self.placement}>"
    def get_placement(self):
        return self.placement
    def set_left(self, component):
        self.left = component
    def set_right(self, component):
        self.right = component
    def get_options(self):
        # print(self,self.left, self.right)
        if(not self.options):
            left = 1
            right = 1
            if(self.left):
                left = self.left.get_options()
            if(self.right):
                right = self.right.get_options()
            self.options = left+right
            return left+right
        return self.options
    def get_children(self):
        print(self, "getting children")
        left = 0 
        right = 0
        if(self.left):
            left = 1+self.left.get_children()
        if(self.right):
            right = 1+self.right.get_children()
        return left+right
        
    
class Row():
    def __init__(self, length):
        self.length = length
        self.lasers = {}
        self.splitters = {}
        self.split_count  = 0
    def add_splitter(self, placement):
        self.splitters[placement] = Component("splitter", placement)
    def add_laser(self, placement):
        if( placement not in self.splitters):
            self.lasers[placement] = Component("laser",placement)
        else:
            self.split_laser(placement)
    def get_outputs(self):
        return self.lasers 
    def calc_lasers(self, lasers):
        # print(self.lasers)
        for ind, val in lasers.items():
            # print("ind, val", ind, val, val.get_placement())
            place = val.get_placement()
            if place in self.lasers:
                continue 
            if place in self.splitters:
                
                self.split_laser(place)
                continue 
            self.add_laser(place)
                # print("laser gonna hit splitter")
    def split_laser(self, place):
        self.split_count += 1
        # print("creating split at ", place)
        self.add_laser(place-1)
        self.add_laser(place+1)
    def print_row(self):
        start = "." * self.length
        for laser in self.lasers:
            # print(laser)
            start = replace_index(start, "|", laser)
        for splitter in self.splitters:
            # print(splitter)
            start = replace_index(start, "^", splitter)
        return start 
    def get_placement(self, placement):
        if placement in self.splitters:
            return self.splitters[placement]
        return None
    

def replace_index(orig, new_val, index):
    return orig[:index] + new_val + orig[index+1:]

class Field():
    def __init__(self, row):
        self.rows = {0:row}
        self.max_depth = 0
    def parse_row(self, txt):
        length = len(txt.strip())
        # print(length)
        output = Row(length)
        # print(txt.strip())
        for placement, val in enumerate(list(txt.strip())):
            if val == "^":
                output.add_splitter(placement)
        self.max_depth += 1
        self.rows[self.max_depth] = output
    def get_next(self, depth, placement):
        
        found = None
        i = 1
        while not found:
            if depth + i in self.rows:
                found = self.rows[depth+i].get_placement(placement)
                i += 1
            else:
                break
        return found 
    def populate_rows(self):
        for depth, row in self.rows.items():
            # print('hi')
            for placement, splitter in row.splitters.items():
                left = self.get_next(depth, placement -1)
                right = self.get_next(depth, placement + 1)
                
                splitter.set_left(left)
                splitter.set_right(right)
                # print(depth, splitter, splitter.left, splitter.right)
    
with open("input.txt", "r") as f:
    lines = f.readlines()
    field = Field(Row(lines[0]))
    placement = lines[0].index("S")
    for line in lines[1:]:
        # print(line)
        field.parse_row(line)
    print("populating rows")
    field.populate_rows()
    print("done populating")
    
    print("Total:",field.get_next(0, placement).get_options(),)
    
    