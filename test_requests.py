import requests

url = "http://127.0.0.1:5000/ask"

question = {
    "question": "I want a healthy breakfast"
}

response = requests.post(
    url,
    json=question
)

print(response.status_code)
print(response.json())