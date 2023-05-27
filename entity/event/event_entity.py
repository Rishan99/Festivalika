class EventEntity:
    def __init__(self, id, name, title, address, description, startDate, endDate, price, createdDate):
        self.id = id
        self.title = title
        self.address = address
        self.description = description
        self.startDate = startDate
        self.endDate = endDate
        self.price = price
        self.createdDate = createdDate

# Class Method, access by Gender.fromMap(), can access and modify class state, where static method cannot
    @classmethod
    def fromMap(self, map):
        name = map.get('name')
        id = map.get('id')
        return self(id, name)