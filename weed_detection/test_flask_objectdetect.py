from flask import Flask

import requests

BASE_URL = 'http://127.0.0.1:5000'

test_data = {'data': 8}
response = requests.post("{}/predict".format(BASE_URL), json = test_data)
print(response.json())

#If you get error: Response 405 
# Probably the server is getting GET request instead of POST