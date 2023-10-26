#Generator Method 1
gen = (i for i in range(22,27))

for i in gen:
    print(i)
print(type(gen))

#Generator Method 2
def my_gen():
    for i in range(10):
        yield i

for j in my_gen():
    print(j)