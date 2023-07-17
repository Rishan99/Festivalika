class TicketPaymentEntity:
    def __init__(self, id,ticketStatusId,ticketStatus,eventId,eventTitle,userId,userName,createdDate,price,address):
        self.id = id
        self.ticketStatusId = ticketStatusId
        self.ticketStatus = ticketStatus
        self.eventId = eventId
        self.eventTitle = eventTitle
        self.userId = userId
        self.userName = userName
        self.createdDate = createdDate
        self.price = price
        self.address = address        

    @classmethod
    def fromMap(self, data):
        map=dict(data)
        return self(map.get('id'),map.get('ticketStatusId'),map.get('ticketStatus'),map.get('eventId'),
                    map.get('eventTitle'),map.get('userId') ,map.get('userName'),map.get('createdDate'),map.get('price'),map.get('address'))