import time
import redis
from flask import Flask
import csv
import requests
import json


response = requests.get('https://reqres.in/api/unknown/')

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)

def load_data():
    with open ('init.txt') as data_file:
        load_data = csv.reader(data_file)
        for i in load_data:
            if i[1] not in cache:
                cache.set(i[0], i[1])

def get_value(inKey):
    retries = 5
    while True:
        try:
            return cache.scard(inKey)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/default/<input>')
def default(input):
    load_data()
    val = str(cache.get(input))
    response = requests.get('https://reqres.in/api/users/'+val)
    return(response.content.decode('utf-8'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)