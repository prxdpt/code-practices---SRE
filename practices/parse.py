import requests

response = requests.get("https://api.github.com/repos/kubernetes/kubernetes/pulls")

details = response.json()


for i in range(len(details)):
    print(i)
    print(details[i]["user"]["login"])