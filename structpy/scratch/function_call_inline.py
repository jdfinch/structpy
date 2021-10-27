

def average(l):
    total = 0
    for e in l:
        total += e
    return total


ls = [1, 2, 3, 4]
a = average(ls)
print(a, 'is the avg of', ls)

## vs ##

ls = [1, 2, 3, 4]
with average:
    l = ls
    total = 0
    for e in l:
        total += e
    a = total
print(a, 'is the avg of', ls)

