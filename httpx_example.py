import httpx
#
# response = httpx.get("https://jsonplaceholder.typicode.com/todos/1")
#
# print(response.json())
# print(response.status_code)
#
# data = {
#     "title" : "New Title",
#     "completed" : False,
#     "userId" : 1
# }
# response = httpx.post("https://jsonplaceholder.typicode.com/todos")
#
# print(response.status_code)
# print(response.json())
#
# headers = {"Authorization": "Bearer 123"}
# response = httpx.get("https://httpbin.org/get", headers=headers)
#
# print(response.status_code)
# print(response.json())
#
# import httpx
#
# params = {"userId": 1}
#
# response = httpx.get("https://jsonplaceholder.typicode.com/todos", params=params)
#
# print(response.url)    # https://jsonplaceholder.typicode.com/todos?userId=1
# print(response.json()) # Фильтрованный список задач

with httpx.Client() as client:
    response1 = client.get('https://jsonplaceholder.typicode.com/todos/1')
    response2 = client.get('https://jsonplaceholder.typicode.com/todos/2')

print(response1.json())
print(response2.json())

