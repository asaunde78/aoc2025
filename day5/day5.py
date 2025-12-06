import random 

class Range():
    def __init__(self, s = "0-1"):
        start, end = s.split("-")
        self.start = int(start)
        self.end = int(end)
    def __repr__(self):
        return str(self)
    def fill(self, start, end):
        self.start = start 
        self.end = end
        return self
    def num_in_range(self, num):
        return num <= self.end and num >= self.start
    
    def get_nums(self):
        # print(self.start, self.end)
        return list(range(self.start, self.end + 1))
    def __str__(self):
        return f"<{self.start}-{self.end}>"
    
    def can_merge(self, rng):
        in_case = rng.num_in_range(self.start - 1) or rng.num_in_range(self.end + 1)
        out_case = self.num_in_range(rng.start-1) or self.num_in_range(rng.end+1)
        return in_case or out_case
    
    def merge_range(self, rng):
        start = self.start 
        if(self.start > rng.start):
            start = rng.start 
        end = self.end
        if(self.end < rng.end):
            end = rng.end 
        return Range().fill(start, end)
    
    def merge_to_list(self, li):
        ranges = li.copy()
        for saved in ranges:
            if self.can_merge(saved):
                # print("found a range i can merge", self, saved)
                ranges.remove(saved)
                new_range = self.merge_range(saved)
                return new_range.merge_to_list(ranges) 
        ranges.append(self)
        return ranges
    def len_nums(self):
        # print(self.end+1, self.start)
        return (self.end+1) - self.start
            
    
def part1():
    with open("input.txt", "r") as f:
        
        line = f.read().split("\n")
        # print(line)
        start = line.index("")
        ranges = line[:start]
        ranges = list(map(lambda x: Range(x), ranges))
        
        
        ids = line[start+1:]
        total = 0
        for i in ids:
            # found = False
            for r in ranges:
                num = int(i)
                if(r.num_in_range(num)):
                    # print("True", i, r)
                    found = True
                    total += 1
                    break
        
        print(total)
            # if not found:
            #     print("False", i)
            
# part1()

def gen_rand_range(m, tier):
    start = random.randint(0+tier, m+tier)
    diff = random.randint(1, m // 2)
    return Range().fill(start, start+diff)
def get_range(multi):
    start = multi
    end = multi+1
    return Range().fill(start,end)
def part2():
    with open("input.txt", "r") as f:
        
        line = f.read().split("\n")
        # print(line)
        start = line.index("")
        ranges = line[:start]
        ranges = list(map(lambda x: Range(x), ranges))
        og_ranges = ranges.copy()
        # ranges=[ gen_rand_range(20000, random.randint(1000000, 4000000)) for i in range(20)]
        # ranges=[ get_range(i) for i in range(0, 30, 3)]
        # ranges.append(Range().fill(0, 15))
        total = 0
        saved_ranges = []
        for r in ranges:
            print("SR", saved_ranges, "adding r:", r)
            saved_ranges = r.merge_to_list(saved_ranges)
        saved_ranges.sort(key=lambda x: x.end)
        # print(saved_ranges)
        # total = 0
        # for r in saved_ranges:
        #     print(r.len_nums(), r)
        #     total += r.len_nums()
        # print(total, "------------")
        
        
        for r in og_ranges:
            for j in saved_ranges:
                print(r,j)
        # total = 0
        # for r in saved_ranges:
        #     total += len(r.get_nums())
        # print(total)
       
        #379057036794266  not right   
           
part2()
    
    
    
    
    