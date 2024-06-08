import requests as rq
import json as js
import getpass as gp


def print_json(data):
    print(js.dumps(data, indent=2))


endpoint = "http://127.0.0.1:8000/accounts/"


def detail(id: int):
    response = rq.get(endpoint + str(id) + "/")
    if response.status_code == 404:
        print("Post not found")
        exit()
    return response.json()

def signup():
    email = input("Email: ")
    username = input("Username: ")
    password = gp.getpass("Password: ")
    data = {
        "email": email,
        "username": username,
        "password": password
    }
    response = rq.post(endpoint + "signup/", json=data)
    return response.json()

print_json(signup())