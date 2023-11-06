import redis
import json

rd = redis.Redis(host='localhost', port=6379, password='', db=0)

with open('/home/misam/MyGithub/Shop/redis/persons.json') as p:
    data = json.load(p)

with rd.pipeline() as pipe:
    for id, person in enumerate(data, start=1):
        rd.hsetnx("persons", id, str(person))
    pipe.execute()