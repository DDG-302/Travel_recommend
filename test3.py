from socket import timeout
import requests
import json


import urllib


url = "https://cms.lonelyplanet.com/graphql?operationName=PartnerActivityListItemsQuery&variables=%7B%22limit%22%3A20%2C%22offset%22%3A40%2C%22filter%22%3A%7B%22canonicalCategory%22%3A%5B%5D%2C%22duration%22%3A%7B%22maximum%22%3A3%2C%22unit%22%3A%22DAYS%22%7D%2C%22placeId%22%3A%22359279%22%2C%22price%22%3A%7B%22minimum%22%3A1%2C%22currency%22%3A%22USD%22%7D%7D%2C%22page%22%3A2%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%223e99f838d450d9e350817e638a034a5ffe469a7450da61cca96ab77f50054ea2%22%7D%7D"

# print(urllib.parse.unquote(url))
# print(urllib.parse.unquote("https://cms.lonelyplanet.com/graphql?operationName=PartnerActivityListItemsQuery&variables=%7B%27limit%27%3A+20%2C+%27offset%27%3A+40%2C+%27filter%27%3A+%7B%27canonicalCategory%27%3A+%5B%5D%2C+%27duration%27%3A+%7B%27maximum%27%3A+3%2C+%27unit%27%3A+%27DAYS%27%7D%2C+%27placeId%27%3A+%27359279%27%2C+%27price%27%3A+%7B%27minimum%27%3A+1%2C+%27currency%27%3A+%27USD%27%7D%7D%2C+%27page%27%3A+2%7D&extensions=%7B%27persistedQuery%27%3A+%7B%27version%27%3A+1%2C+%27sha256Hash%27%3A+%273e99f838d450d9e350817e638a034a5ffe469a7450da61cca96ab77f50054ea2%27%7D%7D"))
# # print(url.replace("%22", "%27"))
# exit()

# https://cms.lonelyplanet.com/graphql    
# ?operationName=PartnerActivityListItemsQuery        
# &variables={"limit":20,"offset":40,"filter":{"canonicalCategory":[],"duration":{"maximum":3,"unit":"DAYS"},
#           "placeId":"359279","price":{"minimum":1,"currency":"USD"}},"page":2}        
# &extensions={"persistedQuery":{"version":1,"sha256Hash":"3e99f838d450d9e350817e638a034a5ffe469a7450da61cca96ab77f50054ea2"}}

url2 = "https://cms.lonelyplanet.com/graphql"

filter_obj = {
        "canonicalCategory":[],
        "duration":{
            "maximum":3,
            "unit":"DAYS"
        },
        "placeId":"359279",
        "price":{
            "minimum":1,
            "currency":"USD"
        },
}

variables_obj = {
    "limit":20,
    "offset":40,
    "filter":filter_obj,
    "page":2
}

persistedQuery_obj = {
    "version":1,
    "sha256Hash":"3e99f838d450d9e350817e638a034a5ffe469a7450da61cca96ab77f50054ea2"
}

extension_obj = {
    "persistedQuery" : persistedQuery_obj
}

# extension_obj = "\
#     \"persistedQuery\":{\
#         \"version\":1,\
#         \"sha256Hash\":\"3e99f838d450d9e350817e638a034a5ffe469a7450da61cca96ab77f50054ea2\"\
#     }\
# "
# print(str(persistedQuery_obj))
# print(str(json.dumps(str(persistedQuery_obj))))
# print(urllib.parse.urlencode(persistedQuery_obj).encode("utf-8") )
# exit()
# variables_obj = "\
# \"limit\":20, \
#     \"offset\":40, \
#     \"filter\":{ \
#         \"canonicalCategory\":[], \
#         \"duration\":{ \
#             \"maximum\":3, \
#             \"unit\":\"DAYS\" \
#         }, \
#         \"placeId\":\"359279\", \
#         \"price\":{ \
#             \"minimum\":1, \
#             \"currency\":\"USD\" \
#         }, \
#     }, \
#     \"page\":2 \
# "


# print(urllib.parse.urlencode(variables_obj).encode("utf-8") )
# print(urllib.parse.urlencode(test_json).encode("utf-8") )


# params = {
#     "operationName" : "PartnerActivityListItemsQuery",
#     "variables" : variables_obj,
#     "extensions" : extension_obj
# }

params = {
    "operationName" : "PartnerActivityListItemsQuery",
    "variables" : {
        "limit":20,
        "offset":40,
        "filter":{
                "canonicalCategory":[],
                "duration":{
                    "maximum":3,
                    "unit":"DAYS"
                },
                "placeId":"359279",
                "price":{
                    "minimum":1,
                    "currency":"USD"
                },
        },
        "page":2
    },
    "extensions" : {
        "persistedQuery" : {
            "version":1,
            "sha256Hash":"3e99f838d450d9e350817e638a034a5ffe469a7450da61cca96ab77f50054ea2"
        }
    }
}

headers={
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Origin": "https://www.lonelyplanet.com",
    "Referer": "https://www.lonelyplanet.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69"
}

params = urllib.parse.urlencode(params).encode("utf-8") 
params = str(params, encoding="utf-8")
print(params)
params = bytes(params.replace("%27","%22"), encoding="utf-8")
print(params)


# exit()

# exit()
# test = url2 + "?" + str(params)
# print(urllib.parse.unquote(test).encode("utf-8").decode("utf-8"))
# print(urllib.parse.unquote(url))
# print(url == test)
# params = json.dumps(params)
# print(json.loads(params))
# exit()

req = requests.get(url2, timeout=20, headers=headers, params=params)
# req = requests.get(url, timeout=20)
print(req.url)
# msg = req.text.encode('utf-8').decode('unicode_escape')
with open("exp_data.json", "w", encoding="utf-8") as f:
    f.write(req.text)


