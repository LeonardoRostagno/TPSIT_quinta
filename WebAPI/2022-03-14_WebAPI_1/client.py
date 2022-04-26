import requests

# requests 1
r1 = requests.get('http://127.0.0.1:5000/api/v1/resources/books/all')
print(r1.json())

id = input("Inserire l'id [0 1 2]: ")

# requests 2
r2 = requests.get(f'http://127.0.0.1:5000/api/v1/resources/books?id={id}')
print(r2.json())