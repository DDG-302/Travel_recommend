import pyodbc
from model.Attraction import Attraction
from model.Experience import Experience
from pydantic import BaseModel


class SQLServer_dbhelper:
    def __init__(self, table:str, server:str, database:str, uid:str, pwd:str) -> None:
        self.table = table
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + 
        ';DATABASE=' + database + ';UID=' + uid + ';PWD=' + pwd, autocommit=True)
    

    def insert_data(self, model:BaseModel):
        pass

    def delete_data(self, idx:int):
        pass

    def select_data(self, model:BaseModel):
        pass

    def excute_update(self, sql:str, values:tuple=None)->int:
        '''
        执行sql，返回受影响的行
        '''
        try:
            cur = self.connection.cursor()
            if(values != None):
                cur.execute(sql, values)
            else:
                cur.execute(sql)
            self.connection.commit()
            return cur.rowcount
        except pyodbc.Warning as e:
            print("数据库错误")
            print(str(e))
        except BaseException as e:
            print("非数据库错误")
            print(str(e))

    def excute_query(self, sql:str, values:tuple=None)->list:
        '''
        执行sql，返回查询到的list \n
        rows = [row, row, ...] \n
        row可以row[0]取值，也可以row.id这样取值
        '''
        try:
            cur = self.connection.cursor()
            if(values != None):
                data = cur.execute(sql, values).fetchall()
                self.connection.commit()
                return data
            else:
                data = cur.execute(sql).fetchall()
                self.connection.commit()
                return data
        except pyodbc.Warning as e:
            print("数据库错误")
            print(str(e))
        except BaseException as e:
            print("非数据库错误")
            print(str(e))

class Attraction_sqlserver_helper(SQLServer_dbhelper):
    def __init__(self, server: str, uid: str, pwd: str, database: str="Travel_recommend", table: str="attraction") -> None:
        super().__init__(table, server, database, uid, pwd)

    def insert_data(self, attraction_info: BaseModel):
        try:
            cur = self.connection.cursor()
            cur.execute("INSERT INTO " + self.table + " (city, name, score, place) VALUES (?,?,?,?)", (attraction_info.city, attraction_info.name, attraction_info.score, attraction_info.place))
            self.connection.commit()
            return cur.rowcount
        except pyodbc.Warning as e:
            print("数据库错误")
            print(str(e))
        except BaseException as e:
            print("非数据库错误")
            print(str(e))

    def get_attraction_by_name(self, name:str)->list:
        '''
        查询数据 \n
        输入景点名\n
        返回：查询到的信息列表，其中的数据类型是sqlite3.Row
        '''
        sql = "SELECT * FROM "+ self.table +" WHERE name="
        values = (name,)
        return super().excute_query(sql, values)


class Experience_sqlserver_helper(SQLServer_dbhelper):
    def __init__(self, server: str,  uid: str, pwd: str, database: str="Travel_recommend", table: str="experiences") -> None:
        super().__init__(table, server, database, uid, pwd)

    def insert_data(self, experience_info:Experience):
        try:
            cur = self.connection.cursor()
            cur.execute("INSERT INTO " + self.table + " (category, name, city) VALUES (?,?,?)", (experience_info.category, experience_info.name, experience_info.city))
            self.connection.commit()
            return cur.rowcount
        except pyodbc.Warning as e:
            print("数据库错误")
            print(str(e))
            return -2
        except BaseException as e:
            print("非数据库错误")
            print(str(e))
            return -2

