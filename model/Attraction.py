from pydantic import BaseModel


class Attraction(BaseModel):
    '''
    idx : 自增主键 \n
    city : 城市，如france/paris \n
    name : 景点，如Eiffel Tower \n
    score : 评分 \n
    place : 城市内位置，如Eiffel Tower & Western Paris
    '''
    idx:int = 0
    city:str = ""
    name:str = ""
    score:str = ""
    place:str = ""
