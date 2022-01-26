from cv2 import split
from fastapi import FastAPI, Form, Body, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from urllib.parse import unquote
from model.Search_info import Search_info
from DAO.SQLServer import SQLServer_dbhelper
from BLL.Search_data import Search_get
from typing import List


app = FastAPI()
# 解决跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)





@app.get("/search")
def search(search_data:str, page_num:int, offset:int):
    search_data = search_data.split()
    print(search_data)
    search_info = Search_info(search_data=search_data, page_num=page_num, offset=offset)
    data = Search_get().search_info_fromDB(search_info)
    attraction_data = []
    experience_data = []
    for row in data[0]:
        attraction_data.append([row.city, row.score, row.name])
    for row in data[1]:
        experience_data.append([row.city, row.name])
    rtn_msg = {
        "attraction":attraction_data,
        "experience":experience_data
    }
    return rtn_msg



if __name__ == '__main__':   
    uvicorn.run(app = app, host = "0.0.0.0", port = 8001)

    