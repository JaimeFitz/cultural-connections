import requests

url = 'https://collectionapi.metmuseum.org/public/collection/v1'

response = requests.get(url)

print(response.json())