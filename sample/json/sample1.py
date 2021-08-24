import json
import urllib.request
import requests
result = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
print(result)

# sample 1
url = "https://sample.com/sample.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read())
print(data)

# sample2 (better)
r = requests.get(url)
r.encoding='utf-8-sig'
print(r.json())
