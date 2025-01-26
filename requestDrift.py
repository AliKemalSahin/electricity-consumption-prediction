import requests

url = "http://electricity.prediction.local/drift/electricity"

response = requests.get(url)

if response.status_code == 200:
    print("Başarili istek!\n")
    print(response.json())

else:
    print("Hata oluştu:", response.status_code)
