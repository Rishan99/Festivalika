import sqlite3


class EventEntity:
    def __init__(self, id, title, address, description, startDate, endDate, price, createdDate):
        self.id = id
        self.title = title
        self.address = address
        self.description = description
        self.startDate = startDate
        self.endDate = endDate
        self.price = price
        self.createdDate = createdDate

# Class Method, access by Entity.fromMap(), can access and modify class state, where static method cannot
    @classmethod
    def fromMap(self, data:sqlite3.Row):
        map=dict(data)
        return self(id, map.get('title'),map.get('address'),map.get('description'),map.get('startDate'),map.get('endDate'),map.get('price'),map.get('createdDate'))