


from entity.event.event_detail_entity import EventDetailEntity
from entity.event.event_entity import EventEntity
from services.database_helper import DatabaseHelper



class EventService:
    def __init__(self):
        self.databaseHelper=DatabaseHelper()
        
    def getEventById(self,id:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Event WHERE id = ? LIMIT 1''', [id])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            raise Exception ("Event Not Found")
        return EventEntity.fromMap(value)            

    def addEvent(self,event:EventEntity,categoryIds:list):    
        if(len(event.title.strip())==0 or len(event.address.strip())==0):
            raise Exception("Sorry, Title or Address cannot be empty")  
        cur= self.databaseHelper.con.cursor()
        cur1=cur.execute('''INSERT INTO Event (title,description,startDate,endDate,price,address) VALUES (?,?,?,?,?,?)''', [event.title,event.description,event.startDate,event.endDate,event.price,event.address])
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
        cur1=cur.execute('''UPDATE Event SET title = ? description = ? startDate = ? endDate = ? price = ? address = ? WHERE id = ?''',
                         [event.title,event.description,event.startDate,event.endDate,event.price,event.address,event.id])
        eventId = cur1.lastrowid
        cur.execute('DELETE FROM EventCategoryAssociation WHERE EventId = ?',[event.id])
        for categoryId in categoryIds:
            cur.execute('''INSERT INTO EventCategoryAssociation (categoryId,eventId) VALUES (?,?)''',[categoryId,eventId])
        cur.connection.commit()
        cur.close()           

    def getEventByIdWithTicketStatus(self,id:int,userId:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.*,tp.TicketStatusId as ticketStatusId, ts.Name as ticketStatusName from Event e 
                    INNER JOIN TicketPayment tp on tp.eventId = e.Id
                    INNER JOIN TicketStatus ts on ts.id = tp.ticketStatusId
                    WHERE e.id = ? AND e.userId = ? LIMIT 1''', [id,userId])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            raise Exception ("Event Not Found")
        return EventDetailEntity.fromMap(value)   
    
    def deleteEvent(self,id:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''DELETE Event WHERE id = ?''', [id])
        cur.connection.commit()
    
    # This retrieves all the events
    def getEventList(self)->list:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Event''', )
        values =cur.fetchall()
        return list(map(lambda x:EventEntity.fromMap(x),values)) 
    
    
    # This retrieves event to display to user, only events that has not ended will be retrived
    def getEventListForUser(self,currentDate)->list:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Event where endDate>=?''',[str(currentDate)] )
        values =cur.fetchall()
        return list(map(lambda x:EventEntity.fromMap(x),values)) 
   
    def getFilteredEventList(self,query:str,categoryId:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.* from Event e INNER JOIN EventCategoryAssociation eca on eca.eventId = e.id WHERE eca.categoryId =? AND e.address Like '%?%' ''',[categoryId,query.strip()] )
        values =cur.fetchall()
        return list(map(lambda x:EventEntity.fromMap(x),values) )
        
    def allowToByTicket(self,eventId:int)->bool:
        return True
              
                      
   
 