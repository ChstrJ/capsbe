import requests
import time

url = "https://emergeton-api.onrender.com/"

while True:
    res = requests.get(url)
    print(res)
    time.sleep(5)