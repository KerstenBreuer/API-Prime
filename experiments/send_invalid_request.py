import requests

requests.post(
    "http://127.0.0.1:8080/api/v1/greet/",
    json={"greeting": "Hello", "person": 1},
    headers={
        "Content-Type": "application/json",
    },
)