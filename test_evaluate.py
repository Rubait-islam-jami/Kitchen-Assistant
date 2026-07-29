import requests

url = "http://localhost:5000/evaluate"

data = {
    "question": "I want a healthy breakfast",
    "answer": "Try oatmeal with fruits.",
    "relevance": 5
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)