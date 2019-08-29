import re

with open('test.txt', encoding='utf-8') as txt:
    lines = txt.readlines()
i = 0
for line in lines:
    proc = re.search("(\d{7}[-]\d{2}[.]\d{4}[.]\d{1}[.]\d{2}[.]\d{4})",line)
    if proc:
        i += 1
        print(proc.group(0))
j = 0
for line in lines:
    # oab = re.search("[(]\w{3}\s(\d+)\w{0,1}[/]\w{2}[)]",line)
    oab = re.search("[O][A][B]\s(\d+)\w{0,1}[/]\w{2}",line)
    
    if oab:
        j += 1
        print(oab.group(0))
print(i,' ',j)