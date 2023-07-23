from entity.category_entity import CategoryEntity
from entity.gender_entity import GenderEntity
from entity.user_entity import UserEntity
from services.database_helper import DatabaseHelper

class GeneralService:
    def __init__(self):
        self.databaseHelper=DatabaseHelper()
    
    def getGenderList(self)->bool:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Gender''')
        value =cur.fetchall()
        cur.close()
        return list(map(lambda x: GenderEntity.fromMap(x),value))
    
    def getUserList(self)->bool:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from User''')
        value =cur.fetchall()
        cur.close()
        return list(map(lambda x: UserEntity.fromMap(x),value))    

    def getCategoryList(self,)->bool:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Category''')
        value =cur.fetchall()
        cur.close()
        return list(map(lambda x: CategoryEntity.fromMap(x),value))    
   
   
    def getHashedString(self,data:str):
        return data

    