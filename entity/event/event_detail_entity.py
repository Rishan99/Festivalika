from entity.event.event_entity import EventEntity


class EventDetailEntity(EventEntity):
    def __init__(self, id, name):
        self.canBuyTicket = False
        self.ticketStatusId = 1
        self.categoryId = 1
        self.categoryName = 1
        self.ticketStatusName=""

# Class Method, access by Gender.fromMap(), can access and modify class state, where static method cannot
    @classmethod
    def fromMap(self, map):
        name = map.get('name')
        id = map.get('id')
        return self(id, name)