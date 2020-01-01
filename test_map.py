import operator
a={"N":10, "E":2, "S":2, "W":1000}


b = sorted(a.items(), key=operator.itemgetter(1))
print(b)
s = [item for item in b[0][0]]
print(s[0])