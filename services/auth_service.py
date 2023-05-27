
from model.user import User
from services.database_helper import DatabaseHelper


class AuthService:
    def __init__(self):
        self.databaseHelper=DatabaseHelper()
    
    def __checkUsernameExists(self,username:str)->bool:
       cur= self.databaseHelper.con.cursor()
       cur.execute('''SELECT COUNT(Id) as count from User WHERE username = ?  LIMIT 1''', [username])
       value =cur.fetchone()
       cur.close()
       return int(value) >0
        
   
    def loginUser(self,username:str, password:str):
        if(len(username.strip())==0 or len(password.strip())==0):
            raise Exception("Sorry, Username or password cannot be empty")  
        if(not self.__checkUsernameExists(username)):
            raise Exception("Sorry, Username doesnot exists")  
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from User WHERE username = ? AND password=?  LIMIT 1''', [username,password])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            raise Exception ("Username or password is incorrect")
        return User.fromMap(value)
            
    def registerUser(self,user:User):
        
        if(len(user.username.strip())==0 or len(user.password.strip())==0):
            raise Exception("Sorry, Username or password cannot be empty")  
        if(self.__checkUsernameExists(user.username)):
            raise Exception("Sorry, Username already exists")  
        cur= self.databaseHelper.con.cursor()
        cur.execute('''INSERT INTO User (Name,Username,Address,Age,Gender,Password) VALUES (?,?,?,?,?,?)''', [user.name,user.username,user.address,user.age,user.gender,user.password])
        self.databaseHelper.con.commit()
        cur.close()   
                   

   
    