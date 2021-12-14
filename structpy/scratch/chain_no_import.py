
a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]

l = [a, b, c]

chain = lambda l: [y for x in l for y in x]

l_chain = chain(l)

print(l_chain)