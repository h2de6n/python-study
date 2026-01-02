import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

res = requests.get(url, headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
# print(soup.title)
# print(soup.title.get_text())
# print(soup.a)

# print(soup.prettify())

if soup.a:
    # print(soup.a.attrs)
    print(soup.a["href"])
else:
    print("태그 못찾았어.")


print(soup.find("a", attrs={"class": "u_skip"}))
