def get_col(cols, index):
    output = ""
    op = None
    for row in cols:
        if(row[index] not in ["+","*"]):
            output += row[index]
        else:
            op = row[index]
            if(op  == "+"):
                op = lambda x, y: x+y 
            if(op  == "*"):
                op = lambda x, y: x*y
    if(not output.isspace()):
        output = int(output)
    else:
        output = None
    return output, op
with open("input.txt", "r") as f:
    file = f.readlines()
    cols = []
    for line in file:
        clean = line.replace("\n", "")
        cols.append(list(clean))
    # print(len(cols))
    total = 0
    
    i = 0
    while i < len(cols[0]):
        # print(i, "i")
        local_total, op = get_col(cols, i)
        if not local_total:
            i += 1
            continue
        j = 1
        
        val, _op = get_col(cols,i+j)
        # print(val, i, "i", local_total)
        while val:

            # print(j, "j", val)
            local_total = op(val, local_total)
            j += 1
            # print("\t",val, i+j)
            if(i+j >= len(cols[0])):
                i+= j
                break
                
            val, _op = get_col(cols, i+j)
        i+= j 
        # print("final i:", i)
        print("FINAL LOCAL:", local_total )
        total += local_total 
    print("FINAL TOTAL: ", total)
                

    