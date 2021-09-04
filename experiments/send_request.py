import requests

response = requests.post(
    "http://127.0.0.1:8080/api/v1/greet/en",
    json={"greeting": "Hello", "person": "world"},
    headers={
        "Content-Type": "application/json",
    },
    params={"informal": "true"},
)

print(response.json())
