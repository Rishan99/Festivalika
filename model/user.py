class User:
    def __init__(self, name,username,address,age,gender,password=None,id=None,):
        self.name = name
        self.username = username
        self.address = address
        self.age = age
        self.gender = gender
        self.id = id
        self.password = password

    @classmethod
    def fromMap(self, map):
        name = map.get('name')
        id = map.get('id')
        username = map.get('username')
        address = map.get('address')
        age = map.get('age')
        gender = map.get('gender')   
        password = map.get('password')        
        return self(name,username,address,age,gender,password,id,)        