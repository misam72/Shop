import requests as req

url = 'https://en.wikipedia.org/wiki/John_Wayne'
r = req.get(url)
print(r.status_code)
print(dir(r))
print(r.text)