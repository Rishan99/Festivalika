from entity.event.event_entity import EventEntity


class EventListEntity(EventEntity):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def fromMap(self, map):
        name = map.get('name')
        id = map.get('id')
        return self(id, name)