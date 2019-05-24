import sys

lines = {line.split()[-1]:line.split()[0] for line in sys.stdin if "total" not in line}

for k,v in lines.items():
    print(int(v.split(",")[0])*"+", k, v)
