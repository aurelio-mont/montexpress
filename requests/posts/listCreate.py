import requests as rq
import json as js


def print_json(data):
    print(js.dumps(data, indent=2))


endpoint = "http://127.0.0.1:8000/post/"


def list(token: str):
    headers = {
        "Authorization": "Bearer " + token,
    }
    response = rq.get(endpoint, headers=headers)
    return response.json()


def create(token: str):
    title = input("Title: ")
    content = input("Content: ")
    data = {
        "title": title,
        "content": content,
    }
    headers = {
        "Authorization": "Bearer " + token,
    }
    response = rq.post(endpoint, headers=headers, json=data)
    return response.json()


option = input("Would you like to list or create? (l/c): ")

token = input("Token: ")

if option.lower() == "l":
    print_json(list(token))
elif option.lower() == "c":
    print_json(create(token))
else:
    print("Invalid option")
