


from entity.event.event_detail_entity import EventDetailEntity
from entity.event.event_entity import EventEntity
from services.database_helper import DatabaseHelper



class EventService:
    def __init__(self):
        self.databaseHelper=DatabaseHelper()
        
    def getEventById(self,id:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Event WHERE Id = ? LIMIT 1''', [id])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            raise Exception ("Event Not Found")
        return EventEntity.fromMap(value)            

    def addEvent(self,event:EventEntity,categoryIds:list):    
        if(len(event.title.strip())==0 or len(event.address.strip())==0):
            raise Exception("Sorry, Title or Address cannot be empty")  
        cur= self.databaseHelper.con.cursor()
        cur1=cur.execute('''INSERT INTO Event (Title,Description,StartDate,EndDate,Price,Address) VALUES (?,?,?,?,?,?)''', [event.title,event.description,event.startDate,event.endDate,event.price,event.address])
        eventId = cur1.lastrowid
        if(eventId == None):
            raise Exception("Error Adding Event, Please Try again")
        for categoryId in categoryIds:
            cur.execute('''INSERT INTO EventCategoryAssociation (CategoryId,EventId) VALUES (?,?)''',[categoryId,eventId])
        cur.connection.commit()
        cur.close()  
        
    def updateEvent(self,event:EventEntity,categoryIds:list):    
        eventInfo = self.getEventById(event.id)
        if(len(event.title.strip())==0 or len(event.address.strip())==0):
            raise Exception("Sorry, Title or Address cannot be empty")  
        cur= self.databaseHelper.con.cursor()
        cur1=cur.execute('''UPDATE Event SET Title = ? Description = ? StartDate = ? EndDate = ? Price = ? Address = ? WHERE Id = ?''',
                         [event.title,event.description,event.startDate,event.endDate,event.price,event.address,event.id])
        eventId = cur1.lastrowid
        cur.execute('DELETE FROM EventCategoryAssociation WHERE EventId = ?',[event.id])
        for categoryId in categoryIds:
            cur.execute('''INSERT INTO EventCategoryAssociation (CategoryId,EventId) VALUES (?,?)''',[categoryId,eventId])
        cur.connection.commit()
        cur.close()           

    def getEventByIdWithTicketStatus(self,id:int,userId:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.*,tp.TicketStatusId as ticketStatusId, ts.Name as ticketStatusName from Event e 
                    INNER JOIN TicketPayment tp on tp.EventId = e.Id
                    INNER JOIN TicketStatus ts on ts.Id = tp.TicketStatusId
                    WHERE e.Id = ? AND e.UserId = ? LIMIT 1''', [id,userId])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            raise Exception ("Event Not Found")
        return EventDetailEntity.fromMap(value)   
    
    def deleteEvent(self,id:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''DELETE  Event WHERE Id = ?''', [id])
        cur.connection.commit()
    
    def getEventList(self):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Event''', )
        values =cur.fetchall()
        return map(lambda x:EventEntity.fromMap(x),values) 
    
    def getFilteredEventList(self,query:str,categoryId:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.* from Event e INNER JOIN EventCategoryAssociation eca on eca.eventId = e.Id WHERE eca.categoryId =? AND e.address Like '%?%' ''',[categoryId,query.strip()] )
        values =cur.fetchall()
        return map(lambda x:EventEntity.fromMap(x),values) 
        
    def allowToBuyTicket(self,eventId:int)->bool:
        return True
              
                      
   
 