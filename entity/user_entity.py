class UserEntity:
    def __init__(self, name,username,address,gender,isAdmin,password:str|None=None,id:None|int=None,):
        self.name = name
        self.username = username
        self.address = address
        self.gender = gender
        self.id = id
        self.password = password
        self.isAdmin = isAdmin==1

    @classmethod
    def fromMap(self, data):
        map=dict(data)
        name = map.get('name')
        id = map.get('id')
        username = map.get('username')
        address = map.get('address')
        gender = map.get('gender')   
        password = map.get('password') 
        isAdmin = map.get('isAdmin')        
        return self(name,username,address,gender,isAdmin,password,id,)        