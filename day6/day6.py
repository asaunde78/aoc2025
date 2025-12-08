from functools import reduce


def mult(a,b):
    return a * b
def add(a, b):
    return a + b
def get_func(code):
    if code == "+":
        return add
    if code == "*":
        return mult

def part1_conversion(li):
    return [int(i) for i in li]


with open("input.txt", "r") as f:
    file = f.readlines()
    
    operators = []
    cols = []
    for i, line in enumerate(file):
        
        row = line.strip().split()
        if(i == len(file) - 1):
            operators = row
            continue


        if(len(cols) == 0):
            row = [[j] for j in row]
            cols = row
            continue
        for index, item in enumerate(row):
            cols[index].append(item)
    total = 0
    for index, col in enumerate(cols):
        op = operators[index]
        nums = part1_conversion(col)
        
        print(nums, op)
        output = reduce(get_func(op), nums)
        total += output
        
    print("Total: ", total)
