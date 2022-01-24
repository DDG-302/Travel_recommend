from pydantic import BaseModel


class Experience(BaseModel):
    '''
    idx : 自增主键 \n
    category : 分类 \n
    name : 游览项目名称 \n
    city : 城市，如france/paris \n
    '''
    idx:int = 0
    category:str = ""
    name:str = ""
    city:str = ""