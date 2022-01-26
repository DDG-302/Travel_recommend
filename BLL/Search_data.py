from DAO.SQLServer import Attraction_sqlserver_helper, \
                            Experience_sqlserver_helper, \
                            SQLServer_dbhelper
from model.Search_info import Search_info


class Search_get:
    def __init__(self) -> None:
        pass
    
    def search_info_fromDB(self, search_info:Search_info):
        
        for idx in range(len(search_info.search_data)):
            search_info.search_data[idx] = "%" + search_info.search_data[idx] + "%"
        like = " city LIKE ? "    
        idx = 1
        while(idx < len(search_info.search_data)):
            like = like + " OR city LIKE ? "
            idx += 1
        attraction_name_data = Attraction_sqlserver_helper().select_data_by_city(search_info, like)
        experience_name_data = Experience_sqlserver_helper().select_data_by_city(search_info, like)
        return (attraction_name_data, experience_name_data)
