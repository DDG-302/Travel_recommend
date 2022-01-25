from itsdangerous import encoding
import requests
import urllib
import json


url = "https://cms.lonelyplanet.com/graphql"
headers={
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Origin": "https://www.lonelyplanet.com",
    "Referer": "https://www.lonelyplanet.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69"
}
page = 1
offset = 0
params = {
    "operationName" : "PartnerActivityListItemsQuery",
    "variables" : {
        "limit":20,
        "offset":offset,
        "filter":{
                "canonicalCategory":[],
                "duration":{
                    "maximum":3,
                    "unit":"DAYS"
                },
                "placeId":"359279", # 通过placeId搜索不同的地区
                "price":{
                    "minimum":1,
                    "currency":"USD"
                },
        },
        "page":page
    },
    "extensions" : {
        "persistedQuery" : {
            "version":1,
            "sha256Hash":"3e99f838d450d9e350817e638a034a5ffe469a7450da61cca96ab77f50054ea2"
        }
    }
}

i = 0
while( i < 5):
    try:
        encoded_params = urllib.parse.urlencode(params).encode("utf-8")
        encoded_params = str(encoded_params, encoding="utf-8")
        # %27是单引号，%22是双引号
        # 服务端无法解析单引号，要转为双引号再发送请求
        encoded_params = bytes(encoded_params.replace("%27", "%22"), encoding="utf-8")
        req = requests.get(url, headers=headers, timeout=20, params=encoded_params)
        data = json.loads(req.text)
        
        params["page"] = page
        print(req.text)
        with open(str(offset) + "test" + str(page) + ".json", "w", encoding="utf-8") as f:
            # f.write("page:" + str(page) + "\n")
            f.write(req.text)
            f.write("")
        break
    except BaseException as e:
        print(e)
        print("重试")
        i = i+1
    finally:
        if(i >= 5):
            print("超时次数过多")
            exit(-1)
offset = offset+1
while(offset < 2):
    try:
        # params["page"] = page
        params["variables"]["offset"] = offset
        encoded_params = urllib.parse.urlencode(params).encode("utf-8")
        encoded_params = str(encoded_params, encoding="utf-8")
        # %27是单引号，%22是双引号
        # 服务端无法解析单引号，要转为双引号再发送请求
        encoded_params = bytes(encoded_params.replace("%27", "%22"), encoding="utf-8")
        req = requests.get(url, headers=headers, timeout=20, params=encoded_params)
        data = json.loads(req.text)
        
        params["page"] = page
        with open(str(offset) + "test" + str(page) +".json", "w", encoding="utf-8") as f:
            # f.write("page:" + str(page) + "\n")
            f.write(req.text)
            f.write("")
        offset = offset + 1
    except BaseException as e:
        print(e)
        print("重试")
        i = i+1
    finally:
        if(i >= 5):
            print("超时次数过多")
            exit(-1)

