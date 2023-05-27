class User:
    def __init__(self, name,username,address,age,gender,password=None,id=None,):
        self.name = name
        self.username = username
        self.address = address
        self.age = age
        self.gender = gender
        self.id = id
        self.password = password