from entity.event.event_entity import EventEntity


class EventDetailEntity(EventEntity):
    def __init__(self, canBuyTicket, ticketStatusId,categoryId,categoryName,ticketStatusName):
        self.canBuyTicket = canBuyTicket
        self.ticketStatusId =ticketStatusId
        self.categoryId = categoryId
        self.categoryName =categoryName
        self.ticketStatusName=ticketStatusName

    @classmethod
    def fromMap(self, data):
        map=dict(data)
        return self(map.get("canBuyTicket"), map.get("ticketStatusId"), map.get("categoryId"), map.get("categoryName"), map.get("ticketStatusName"))