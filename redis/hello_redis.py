import redis

rd = redis.Redis(host='localhost', port=6379, password='', db=0)

rd.set('name', 'jax')
rd.set('age', 22)

print(rd.get('name'))
print(rd.get('age'))

print(rd.client_list())