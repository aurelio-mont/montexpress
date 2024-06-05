import requests as rq
import json as js


def print_json(data):
    print(js.dumps(data, indent=2))


endpoint = "http://127.0.0.1:8000/post/"


def list():
    response = rq.get(endpoint)
    return response.json()


def create():
    title = input("Title: ")
    content = input("Content: ")
    data = {
        "title": title,
        "content": content,
    }
    response = rq.post(endpoint, json=data)
    return response.json()


option = input("Would you like to list or create? (l/c): ")

if option.lower() == "l":
    print_json(list())
elif option.lower() == "c":
    print_json(create())
else:
    print("Invalid option")
