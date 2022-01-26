from pydantic import BaseModel


class Search_info(BaseModel):
    '''
    search_data : 或关系相连的查询关键词 \n
    page_num : 一次查询获取的数量\n
    offset : 从偏移量开始查询page_num个 \n
    '''
    search_data:list
    page_num:int
    offset:int