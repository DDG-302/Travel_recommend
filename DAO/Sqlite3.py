import sqlite3
from model.Attraction import Attraction
from model.Experience import Experience
from pydantic import BaseModel

class Sqlite3_dbhelper:
    def __init__(self, table, database, path="") -> None:
        self.connection = sqlite3.connect(path + database)
        self.table = table
        self.connection.row_factory = sqlite3.Row

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
                cur.execute(sql, values).fetchall()
            else:
                cur.execute(sql).fetchall()
            self.connection.commit()
            return cur.rowcount
        except sqlite3.IntegrityError as e:
            print("数据库关系一致性错误")
            print(str(e))
        except sqlite3.ProgrammingError as e:
            print("SQL语法错误")
            print(str(e))
        except sqlite3.OperationalError as e:
            print("数据库操作发生错误")
            print(str(e))
        except sqlite3.NotSupportedError as e:
            print("数据库不支持的方法或API")
            print(str(e))
        except BaseException as e:
            print("非数据库错误")
            print(str(e))

    def excute_query(self, sql:str, values:tuple=None)->list:
        '''
        执行sql，返回查询到的list
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
        except sqlite3.IntegrityError as e:
            print("数据库关系一致性错误")
            print(str(e))
        except sqlite3.ProgrammingError as e:
            print("SQL语法错误")
            print(str(e))
        except sqlite3.OperationalError as e:
            print("数据库操作发生错误")
            print(str(e))
        except sqlite3.NotSupportedError as e:
            print("数据库不支持的方法或API")
            print(str(e))
        except BaseException as e:
            print("非数据库错误")
            print(str(e))




class Attraction_dbhelper(Sqlite3_dbhelper):
    def __init__(self, table="attraction", database="LonelyPlanet.db") -> None:
        super().__init__(table, database, path="database/")
        

    def insert_data(self, attraction_info:Attraction):
        try:
            cur = self.connection.cursor()
            cur.execute("INSERT INTO " + self.table + " (city, name, score, place) VALUES (?,?,?,?)", (attraction_info.city, attraction_info.name, attraction_info.score, attraction_info.place))
            self.connection.commit()
            return cur.rowcount
        except sqlite3.IntegrityError as e:
            print("数据库关系一致性错误")
            print(str(e))
        except sqlite3.ProgrammingError as e:
            print("SQL语法错误")
            print(str(e))
        except sqlite3.OperationalError as e:
            print("数据库操作发生错误")
            print(str(e))
        except sqlite3.NotSupportedError as e:
            print("数据库不支持的方法或API")
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

    def is_attraction_exists(self, attraction_name:str)->bool:
        '''
        
        '''
        try:
            cur = self.connection.cursor()
            data = cur.execute("SELECT * FROM "+ self.table +" WHERE name=", (attraction_name,)).fetchall()
            self.connection.commit()
            if(data == None):
                return False
            else:
                return True

        except sqlite3.IntegrityError as e:
            print("数据库关系一致性错误")
            print(str(e))
        except sqlite3.ProgrammingError as e:
            print("SQL语法错误")
            print(str(e))
        except sqlite3.OperationalError as e:
            print("数据库操作发生错误")
            print(str(e))
        except sqlite3.NotSupportedError as e:
            print("数据库不支持的方法或API")
            print(str(e))
        except BaseException as e:
            print("非数据库错误")
            print(str(e))


class Experience_dbhelper(Sqlite3_dbhelper):
    def __init__(self, table="experiences", database="LonelyPlanet.db") -> None:
        super().__init__(table, database, path="database/")

    def insert_data(self, experience_info:Experience):
        try:
            cur = self.connection.cursor()
            cur.execute("INSERT INTO " + self.table + " (category, name, city) VALUES (?,?,?)", (experience_info.category, experience_info.name, experience_info.city))
            self.connection.commit()
            return cur.rowcount
        except sqlite3.IntegrityError as e:
            print("数据库关系一致性错误")
            print(str(e))
        except sqlite3.ProgrammingError as e:
            print("SQL语法错误")
            print(str(e))
        except sqlite3.OperationalError as e:
            print("数据库操作发生错误")
            print(str(e))
        except sqlite3.NotSupportedError as e:
            print("数据库不支持的方法或API")
            print(str(e))
        except BaseException as e:
            print("非数据库错误")
            print(str(e))