from itsdangerous import encoding
import requests
import urllib
import json
from DAO.Sqlite3 import Attraction_dbhelper
from model.Attraction import Attraction


city_list = ["france/paris"]

url = "https://search-api.swiftype.com/api/v1/public/engines/search.json"
headers={
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Host": "search-api.swiftype.com",
    "Origin": "https://www.lonelyplanet.com",
    "Referer": "https://www.lonelyplanet.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69"
}

per_page = 40

for city in city_list:
    page = 1
    params = {
        "document_types[]":"pois",
        "engine_key":"muVz_KxLzdps_EUUECkA",
        "facets[pois][]":"subtypes",
        "filters[pois][ancestor_slugs][]":city,
        "filters[pois][type][]":"See",
        "per_page":per_page,
        "page":page,
        "q": "",
        "sort_field[pois]":"internal_ranking"
    }
    i = 0
    while( i < 5):
        try:
            encoded_params = urllib.parse.urlencode(params).encode("utf-8")
            req = requests.get(url, headers=headers, timeout=20, params=encoded_params)
            data = json.loads(req.text)
            
            params["page"] = page
            with open("attraction.txt", "a", encoding="utf-8") as f:
                f.write("page:" + str(page) + "\n")
                
                
                for attraction in data["records"]["pois"]:
                    attraction_info = Attraction()
                    attraction_info.city = city
                    attraction_info.name = attraction["name"]
                    attraction_info.score = attraction["score"]
                    attraction_info.place = attraction["place"]
                    Attraction_dbhelper().insert_data(attraction_info)
                    msg = "地点：" + attraction["name"] + "  评分" + str(attraction["score"])
                    print(msg)
                    f.write(msg + "\n")
            with open("attr_data_" + str(page) + ".json", "w", encoding="utf-8") as f:
                f.write(req.text)
            break
        except BaseException as e:
            print(e)
            print("重试")
            i = i+1
        finally:
            if(i >= 5):
                print("超时次数过多")
                exit(-1)
    page = page+1
    while(data["record_count"] == per_page):
        try:
            params["page"] = page
            encoded_params = urllib.parse.urlencode(params).encode("utf-8")
            req = requests.get(url, headers=headers, timeout=20, params=encoded_params)
            data = json.loads(req.text)
            with open("attraction.txt", "a", encoding="utf-8") as f:
                f.write("page:" + str(page) + "\n")
                for attraction in data["records"]["pois"]:
                    attraction_info = Attraction()
                    attraction_info.city = city
                    attraction_info.name = attraction["name"]
                    attraction_info.score = attraction["score"]
                    attraction_info.place = attraction["place"]
                    Attraction_dbhelper().insert_data(attraction_info)
                    msg = "地点：" + attraction["name"] + "  评分" + str(attraction["score"])
                    print(msg)
                    f.write(msg + "\n")
            with open("attr_data_" + str(page) + ".json", "w", encoding="utf-8") as f:
                f.write(req.text)
            page = page+1
            print("page:",page)
        except BaseException as e:
            print(e)
            print("重试")
            i = i+1
        finally:
            if(i >= 5):
                print("超时次数过多")
                exit(-1)
