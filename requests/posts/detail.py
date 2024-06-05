import requests as rq
import json as js


def print_json(data):
    print(js.dumps(data, indent=2))


endpoint = "http://127.0.0.1:8000/post/"


def detail(id: int):
    response = rq.get(endpoint + str(id) + "/")
    if response.status_code == 404:
        print("Post not found")
        exit()
    return response.json()


def update(id: int):
    title = input("Title: ")
    content = input("Content: ")
    data = {
        "title": title,
        "content": content,
    }
    response = rq.put(endpoint+str(id)+"/", json=data)
    return response.json()

def delete(id: int):
    response = rq.delete(endpoint+str(id)+"/")
    return response.status_code

id = int(input("ID of post: "))
print_json(detail(id))

option = input("Would you like to update or remove? (u/r): ")
if option.lower() == "u":
    print_json(update(id))
elif option.lower() == "r":
    print(delete(id))
elif option.lower() == "c":
    exit()
else:
    print("Invalid option")
