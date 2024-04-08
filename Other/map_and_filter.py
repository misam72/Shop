''' Q1:
    Given a list of strings: ['apple', 'banana', 'cherry', 'date'], write a Python code using the map 
    function to create a new list that contains the length of each string in the original list.
'''
''' Answer1:
l = ['apple', 'banana', 'cherry', 'date']

def find_len(s):
    return len(s)

m = list(map(find_len, l))
print(m)'''

'''Q2:
    Suppose you have a list of numbers: [10, 20, 30, 40, 50]. Write a Python code using the filter
    function to return a new list containing only the numbers greater than 25, and then use the map
    function to multiply each number in the filtered list by 2.
'''
''' Answer2:
n = [10, 20, 30, 40, 50]
m = list(map(lambda x:x*2, list(filter(lambda x: x>25, n))))
print(m)'''

'''Q3:
    Given a list of integers: [1, 2, 3, 4, 5, 6, 7, 8, 9], write a Python code using the filter 
    function to return a new list that contains only the prime numbers from the original list.
'''
''' Answer3:
n = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def is_prime(n):
    if n < 2:
        return False
    else:
        for i in range(2, int(n ** 0.5) + 1):
            if n%i == 0:
                return False
        return True

p = list(filter(is_prime, n))
print(p)'''

'''Q4:
    Suppose you have a list of sentences: ["Hello, how are you?", "I am fine.", "What about you?",
    "I'm good too."]. Write a Python code using the map function to create a new list that 
    contains the number of words in each sentence from the original list.
'''
''' Answer4:
l = ["Hello, how are you?", "I am fine.", "What about you?", "I'm good too."]

def word_count(s: str):
    w = 1
    for c in s:
        if c == ' ':
            w += 1
    return w

n_words = list(map(word_count, l))
print(n_words)'''

'''Q5:
    Consider a list of dictionaries representing students: [{'name': 'John', 'age': 20},
    {'name': 'Alice', 'age': 18}, {'name': 'Bob', 'age': 22}]. 
    Write a Python code using the filter function to return a new list that contains only the names
    of the students who are above 20 years old.
'''
''' Answer5:
l = [{'name': 'John', 'age': 21}, {'name': 'Alice', 'age': 18}, {'name': 'Bob', 'age': 22}]

std = list(filter(lambda d: d if d['age']>20 else None, l))
std_names = list(map(lambda x: x['name'], l))
print(std_names)'''













