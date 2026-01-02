import requests

url = "https://h2de6n.tistory.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
res = requests.get(url, headers=headers)
res.raise_for_status()

with open("h2de6n.html", "w", encoding="utf8") as f:
    f.write(res.text)
