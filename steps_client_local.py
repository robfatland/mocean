import requests
print(requests.get('http://localhost:8080/steps?message=1.12345').content.decode('utf-8'))
