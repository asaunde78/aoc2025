
def imax(li):
    top = max(li)
    i = li.index(top)
    return i, top 

def list_pop(li, remaining):
    if (len(li) == 0 or remaining == 0 ):
        return []
    # print("length of li", len(li), "remaining", remaining, li)
    # print(remaining-1)
    left = remaining - 1
    options = li[:-(left)] if left > 0 else li
    # print("options: " , options)
    i, top = imax(options)
    # print(i, len(li), remaining)
    output = [top]
    output.extend(list_pop(li[i+1:],remaining-1))
    return output 

def list_to_numbers(li):
    fixed = [str(i) for i in li]
    return int("".join(fixed))

with open("input.txt", "r") as f:
    file = f.readlines()
    total = 0 
    for line in file:
        nums = list(map(lambda x: int(x), list(line.strip())))
        # print(nums)
        answer = list_pop(nums, 12)
        # print("answer", len(answer), answer, list_to_numbers(answer))
        total += list_to_numbers(answer)
        
        
        # short = nums[:-1]
        # i, top = imax(short)
        # first = top 

        # last = nums[i+1:]
        # # print(last)
        # i, top = imax(last)
        # second = top 

        # joltage = 10*first + second 
        # print(joltage)
        # total += joltage 
    print(total)
