from entity.event.event_entity import EventEntity


class EventDetailEntity(EventEntity):
    def __init__(self,id, title, address, description, startDate, endDate, price, createdDate, canBuyTicket, ticketStatusId,categoryId,categoryName,ticketStatusName):
        super().__init__(id, title, address, description, startDate, endDate, price, createdDate,)
        self.canBuyTicket = canBuyTicket == 1
        self.ticketStatusId =ticketStatusId
        self.categoryId = categoryId
        self.categoryName =categoryName
        self.ticketStatusName=ticketStatusName
        

    @classmethod
    def fromMap(self, data):
        map=dict(data)
        return self(map.get('id'), map.get('title'),map.get('address'),map.get('description'),map.get('startDate'),map.get('endDate'),map.get('price'),map.get('createdDate'),map.get("canBuyTicket"), map.get("ticketStatusId"), map.get("categoryId"), map.get("categoryName"), map.get("ticketStatusName"))