class Component():
    def __init__(self, _type, placement):
        self.type = _type
        self.placement = placement
    def get_placement(self):
        return self.placement
 
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
        



def replace_index(orig, new_val, index):
    return orig[:index] + new_val + orig[index+1:]

answer = ""
with open("test.txt", "r") as f:
    lines = f.readlines()
    length = len(lines[0].strip())
    print(length)
    prev = None
    inputs = None
    total = 0
    for depth, line in enumerate(lines):
        print("reference line: ", line)
        new_line = line
        if(depth == 0):
            placement = line.index("S")
            prev = Row(length)
            prev.add_laser(placement)
            continue
        
        inputs = prev.get_outputs()
        # print("inputs:", inputs)
        temp_row = Row(length)
        for placement, val in enumerate(list(line)):
            if val == "^":
                temp_row.add_splitter(placement)
        temp_row.calc_lasers(inputs)
        total += temp_row.split_count
        prev = temp_row
        print(temp_row.print_row())
        # print(temp_row.print_row(), temp_row.get_outputs())
    print("Total: ", total)
    
    

        
