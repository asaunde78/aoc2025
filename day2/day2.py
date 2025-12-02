import re

with open("input.txt", "r") as f:
    file = f.read()
    ranges = file.split(",")
    total = 0
    for _range in ranges:
        first, last = _range.split("-")
        for r in range(int(first), int(last)+1):
            #r"^(.+)(?=\1$)" first solution
            # if re.search(r"^(.+)(?=\1+$)", str(r)):
            #     total += r 
            #second solution
            if re.search(r"^(.+)(?=\1+$)", str(r)):
                total += r 
    print(total)
#^(.*)(\1+)$ apparently this will work too 




