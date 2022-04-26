import requests

id = input("Inserire l'id [0 1 2]: ")
r_id = requests.get(f'http://127.0.0.1:5000/api/v1/resources/books/id?id={id}')
print(r_id.json())

title = input("Inserire il titolo [Il Nome della Rosa - Il Problema dei 3 Corpi - Fondazione]: ")
r_title = requests.get(f'http://127.0.0.1:5000/api/v1/resources/books/title?title={title}')
print(r_title.json())