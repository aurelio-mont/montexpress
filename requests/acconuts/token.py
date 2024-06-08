import requests as rq
import json as js
import getpass as gp


def print_json(data):
    print(js.dumps(data, indent=2))


endpoint = "http://127.0.0.1:8000/accounts/"

def login():
    email = input("Email: ")
    password = gp.getpass("Password: ")
    data = {
        "email": email,
        "password": password
    }
    response = rq.post(endpoint + "token/", json=data)
    return response.json()

print_json(login())