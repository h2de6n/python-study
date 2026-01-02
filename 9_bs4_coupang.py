import requests
from bs4 import BeautifulSoup

url = "https://www.coupang.com/np/search?component=&q=%EB%85%B8%ED%8A%B8%EB%B6%81&traceId=mjwnnlva&channel=user"
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

print(res.text)
