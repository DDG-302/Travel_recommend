import requests
import urllib
import json
# from DAO.Sqlite3 import Attraction_dbhelper, Experience_dbhelper, Sqlite3_dbhelper
from DAO.SQLServer import Attraction_sqlserver_helper, Experience_sqlserver_helper, SQLServer_dbhelper
from model.Attraction import Attraction
from model.Experience import Experience
from pydantic import BaseModel
import copy
import threading


city_list = ["france/paris"]
code_city_pair = {
    "359279" :  "france/paris"
}
server = "LAPTOP-J46PEG2H"
uid = "dingdot"
pwd = "123456"

def write_json(filename, path, data:json):
    with open(path+filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(data))

class Crawler:
    def __init__(self, timeout_times:int=5, max_thread:int=5) -> None:
        self.timeout_count = timeout_times
        self.semaphore = threading.Semaphore(max_thread)
        self.flag = True # 用于控制是否需要继续创建线程

    def get_info(self, url:str, params:dict, headers:str=None)->json:
        while(self.timeout_count > 0 and self.flag):
            try:
                encoded_params = urllib.parse.urlencode(params).encode("utf-8")
                encoded_params = str(encoded_params, encoding="utf-8")
                # %27是单引号，%22是双引号
                # 服务端无法解析嵌套json中的单引号，要转为双引号再发送请求
                encoded_params = bytes(encoded_params.replace("%27", "%22"), encoding="utf-8")
                req = requests.get(url, headers=headers, timeout=20, params=encoded_params)
                self.semaphore.release()
                return json.loads(req.text)

                # for experience in data["data"]["activities"]["entities"]:
                #     experience_info = Experience()
                #     experience_info.name = experience["name"]
                #     experience_info.category = experience["canonicalCategory"]
                #     experience_info.city = "france/paris"
                #     Experience_dbhelper().insert_data(experience_info)
                
            except BaseException as e:
                print(e)
                print("重试")
                self.timeout_count = self.timeout_count-1
                if(self.timeout_count < 0):
                    print("超时次数过多")
                    self.semaphore.release()
                    return None
        return None

    def save_2_db(self, model:BaseModel, sql_dbhelper:SQLServer_dbhelper):
        sql_dbhelper.insert_data(model)


class Attraction_crawler(Crawler):
    def __init__(self, per_page:int=40, init_page:int=1, timeout_times:int=5, max_thread:int=5) -> None:
        super().__init__(timeout_times=timeout_times, max_thread=max_thread)
        self.per_page = per_page
        self.page = init_page
        self.base_params = {
            "document_types[]":"pois",
            "engine_key":"muVz_KxLzdps_EUUECkA",
            "facets[pois][]":"subtypes",
            "filters[pois][ancestor_slugs][]":"",
            "filters[pois][type][]":"See",
            "per_page":per_page,
            "page":init_page,
            "q": "",
            "sort_field[pois]":"internal_ranking"
        }
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Host": "search-api.swiftype.com",
            "Origin": "https://www.lonelyplanet.com",
            "Referer": "https://www.lonelyplanet.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69"
        }
        self.url = "https://search-api.swiftype.com/api/v1/public/engines/search.json"

    def run(self):
        for city in city_list:
            threading.Thread(target=self._run_once, args=(city,)).start() 
            

    def _run_once(self, city):
        while(self.flag):
            params = copy.deepcopy(self.base_params)
            params["page"] = self.page
            params["filters[pois][ancestor_slugs][]"] = city
            self.semaphore.acquire()
            threading.Thread(target=self._search_once, args=(params, city)).start()
            self.page = self.page + 1
        print(city+" 景点搜索完成")

    def _search_once(self, params, city):
        data = json
        if(self.flag):
            data = super().get_info(self.url, params, self.headers)
        if(data == None):
            self.flag = False
            return
        if(data["record_count"] != self.per_page):
            self.flag = False
        json_name = "page_" + str(params["page"]) + ".json"
        write_json(json_name, "json_data/attraction/", data)
        for attraction in data["records"]["pois"]:
            attraction_info = Attraction()
            attraction_info.city = city
            attraction_info.name = attraction["name"]
            attraction_info.score = attraction["score"]
            attraction_info.place = attraction["place"]
            super().save_2_db(attraction_info, Attraction_sqlserver_helper(server=server, uid=uid, pwd=pwd))

class Experience_crawler(Crawler):
    def __init__(self, limit:int=20, init_offset:int=0, request_time:int=5, timeout_times:int=5, max_thread:int=5) -> None:
        super().__init__(timeout_times=timeout_times, max_thread=max_thread)
        self.offset = init_offset
        self.epoch_offset = limit
        self.request_time= request_time
        self.base_params = {
            "operationName" : "PartnerActivityListItemsQuery",
            "variables" : {
                "limit":limit, # 每次获取的信息数量
                "offset":init_offset,
                "filter":{
                        "canonicalCategory":[],
                        "duration":{
                            "maximum":3,
                            "unit":"DAYS"
                        },
                        "placeId":"", # 通过placeId搜索不同的地区
                        "price":{
                            "minimum":1,
                            "currency":"USD"
                        },
                },
                "page":1
            },
            "extensions" : {
                "persistedQuery" : {
                    "version":1,
                    "sha256Hash":"3e99f838d450d9e350817e638a034a5ffe469a7450da61cca96ab77f50054ea2"
                }
            }
        }
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Origin": "https://www.lonelyplanet.com",
            "Referer": "https://www.lonelyplanet.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69"
        }
        self.url = "https://cms.lonelyplanet.com/graphql"

    def run(self):
        for citycode in code_city_pair.__iter__():
            threading.Thread(target=self._run_once, args=(citycode,)).start() 
            
        print("运行结束")

    def _run_once(self, citycode):
        while(self.request_time > 0 and self.flag):
            params = copy.deepcopy(self.base_params)
            params["variables"]["offset"] = self.offset
            params["variables"]["filter"]["placeId"] = citycode
            self.semaphore.acquire()
            threading.Thread(target=self._search_once, args=(params, citycode)).start()
            self.offset = self.offset + self.epoch_offset
            self.request_time -= 1
        print(code_city_pair[citycode]+" 游览搜索完成")

    def _search_once(self, params, citycode):
        data = json
        if(self.flag):
            data = super().get_info(self.url, params, self.headers)
        if(data == None):
            self.flag = False
            return
        json_name = "offset_" + str(params["variables"]["offset"]) + "_limit_" + str(self.epoch_offset) + ".json"
        write_json(json_name, "json_data/experience/", data)
        for experience in data["data"]["activities"]["entities"]:
            experience_info = Experience()
            experience_info.name = experience["name"]
            experience_info.category = experience["canonicalCategory"]
            experience_info.city = code_city_pair[citycode]
            experience_info.short_description = experience["descriptions"]["shortDescription"]
            super().save_2_db(experience_info, Experience_sqlserver_helper(server=server, uid=uid, pwd=pwd)) 


