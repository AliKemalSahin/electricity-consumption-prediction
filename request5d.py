import requests

url = "http://electricity.prediction.local/forecast5d?date=2022-05-23&days=5"

response = requests.get(url)

if response.status_code == 200:
    print("Başarili istek!\n")
    data = response.json()
    predictions = data.get('predictions', {})

    for time, value in predictions.items():
        print(f"{time}: {value}")
else:
    print("Hata oluştu:", response.status_code)
