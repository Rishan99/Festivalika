
from model.user import User
from services.database_helper import DatabaseHelper
from model.gender import Gender


class GeneralService:
    def __init__(self):
        self.databaseHelper=DatabaseHelper()
    
    def getGenderList(self,username:str)->bool:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Gender''')
        value =cur.fetchall()
        cur.close()
        return map(lambda x: Gender.fromMap(x),value)
   
    def getUserById(self,id:str):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from User WHERE Id = ? LIMIT 1''', [id])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            raise Exception (f"User doesnot exists")       
        return User.fromMap(value)  
   
    def getUserByUsername(self,username:str):
       cur= self.databaseHelper.con.cursor()
       cur.execute('''SELECT * from User WHERE username = ? LIMIT 1''', [username])
       value =cur.fetchone()
       cur.close()
       if(value == None):
            raise Exception (f"User with Username {username} not found")       
       return User.fromMap(value)      