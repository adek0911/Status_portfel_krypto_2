import requests

base = "http//127.0.0.1:5000/"

# response = requests.get(base + "test")
response = requests.get("http://127.0.0.1:5000/test")

print(response.json())
