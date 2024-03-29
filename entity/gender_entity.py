class GenderEntity:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# Class Method, access by Gender.fromMap(), can access and modify class state, where static method cannot
    @classmethod
    def fromMap(self, data):
        map=dict(data)
        name = map.get('name')
        id = map.get('id')
        return self(id, name)