import requests

url = "https://community-healthcaregov.p.rapidapi.com/what-is-the-health-insurance-marketplace.json"

headers = {
    'x-rapidapi-host': "community-healthcaregov.p.rapidapi.com",
    'x-rapidapi-key': "4530cb2b74msh6b53c3be454b827p188292jsn9e5ec4781425"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)