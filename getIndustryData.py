file_path_read = "IndustrySectorTickers.txt"
file_path_write = "CorresondingTickersPerIndustry.txt" 
with open(file_path_read, 'r') as f:
    lines = f.readlines()

unique_strings = set()
for line in lines:
    try: 
        split_line = line.strip().split(':')
        unique_strings.add(split_line[-1])
    except:
        print("no")

# with open(file_path, 'w',encoding='utf-8') as f:
#     f.writelines(lines)
addLines = [] 
for line in lines:
    split_line = line.strip().split(':')
    try: 
        if split_line[-1] in unique_strings:
            
            data = split_line[-1] + ":"+ ':'.join(split_line[1:-2])  + '\n'
            unique_strings.remove(split_line[-1])
            addLines.append(data)

    except:
        print("no")
addLines.sort()

with open(file_path_write, 'w',encoding='utf-8') as f:
    f.writelines(addLines)
