

import argon2
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
   
    def getUserById(self,id:str):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from User WHERE id = ? LIMIT 1''', [id])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            raise Exception (f"User doesnot exists")       
        return UserEntity.fromMap(value)  
   
    def getUserByUsername(self,username:str):
       cur= self.databaseHelper.con.cursor()
       cur.execute('''SELECT * from User WHERE username = ? LIMIT 1''', [username])
       value =cur.fetchone()
       cur.close()
       if(value == None):
            raise Exception (f"User with Username {username} not found")       
       return UserEntity.fromMap(value)  
   
    def getHashedString(self,data:str):
        # return argon2.hash_password(data.encode())
        return data

    