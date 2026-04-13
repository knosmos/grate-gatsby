available = set()
for row in open("tmp.txt","r").read().split("\n\n"):
    if "single" in row:
        available.add(row.split()[0].strip())
for row in open("tmp2.txt","r").read().split("\n"):
    if row.split()[0].strip() in available:
        print(row)