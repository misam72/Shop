"""Question 1:
Write a generator function in Python that generates prime numbers indefinitely. A prime number is
a number greater than 1 that is only divisible by 1 and itself. For example, the generator should yield
the sequence: 2, 3, 5, 7, 11, 13, ...
"""
"""Answer 1:"""
'''def gen():
    x = 2
    p = False
    while x<50:
        if x in [2, 3]:
            yield x
        else:
            for i in range(2, int(x**0.5) + 1):
                if x % i == 0:
                    p = False
                    break
                else:
                    p = True
            if p:
                yield x
        x += 1


for g in gen():
    print(g)
'''

'''Q2:
    Write a generator function in Python that generates all permutations of a given list of elements.
    A permutation is an arrangement of elements where the order matters.
    For example, given the list [1, 2, 3], the generator should yield the
    following permutations: [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1].
'''
'''Answer2:'''

'''
def permutations_generator(elements):
    if len(elements) <= 1:
        yield elements
    else:
        for perm in permutations_generator(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]

elements = [1, 2, 3,4]
permutations = permutations_generator(elements)
for perm in permutations:
    print(perm)'''
