from socket import timeout
import requests
headers={
    "Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Host": "search-api.swiftype.com",
"Origin": "https://www.lonelyplanet.com",
"Referer": "https://www.lonelyplanet.com/",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69"
}

url = "https://cdn.acsbapp.com/cache/app/lonelyplanet.com/config.json"

req = requests.get(url, headers=headers, timeout=10)
print(req.text)