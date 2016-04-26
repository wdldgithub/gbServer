from numpy import *
import requests
import json
def datapost(data):
    url = 'http://120.25.86.215:9300/accept/'
    r = requests.post(url, {'data':data})
    return json.loads(r.text)
