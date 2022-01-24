import requests
import json
import urllib


url = "https://www.lonelyplanet.com/france/paris"
url2 = "https://search-api.swiftype.com/api/v1/public/engines/search.json?\
    document_types%5B%5D=pois\
    &engine_key=muVz_KxLzdps_EUUECkA\
    &facets%5Bpois%5D%5B%5D=subtypes\
    &filters%5Bpois%5D%5Bancestor_slugs%5D%5B%5D=france%2Fparis\
    &filters%5Bpois%5D%5Btype%5D%5B%5D=See\
    &per_page=20\
    &q=\
    &sort_field%5Bpois%5D=internal_ranking"
url3 = "https://search-api.swiftype.com/api/v1/public/engines/search.json"

params = {
    "document_types[]":"pois",
    "engine_key":"muVz_KxLzdps_EUUECkA",
    "facets[pois][]":"subtypes",
    "filters[pois][ancestor_slugs][]":"france/paris",
    "filters[pois][type][]":"See",
    "per_page":40,
    "page":1,
    "q": "",
    "sort_field[pois]":"internal_ranking"
}


headers={
    "Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Host": "search-api.swiftype.com",
"Origin": "https://www.lonelyplanet.com",
"Referer": "https://www.lonelyplanet.com/",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69"
}
params = urllib.parse.urlencode(params).encode("utf-8")
# params=json.dumps(params)
print(params)
# req = requests.get(url3, headers=headers, timeout=10, params=params)
# print(req.text)
# print("=================================")
# data = json.loads(req.text) 

json_txt = ""

with requests.get(url3, headers=headers, timeout=20, params=params, stream=True) as data:
        chunk_size = 1024
        start = 1
        # 设置chunk_size让流式文件以块的形式传输
        # 而不是一口气加载全部
        for chunk in data.iter_content(chunk_size):
            json_txt = json_txt + chunk.decode()
            print("下载一个chunk...")
            print(data.url)
        print("\n结束下载")
        # f.write(data.content)

json_file = json.loads(json_txt)
print("=================")
print(json_file)
with open("data3.json", "w") as f:
    f.writelines(json_txt)
# print(data)
