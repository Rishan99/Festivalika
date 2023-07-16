


from datetime import datetime
from entity.category_entity import CategoryEntity
from entity.event.event_detail_entity import EventDetailEntity
from entity.event.event_entity import EventEntity
from services.database_helper import DatabaseHelper

# import services.ticket_payment_service as tp



class EventService:
    def __init__(self):
        self.databaseHelper=DatabaseHelper()
        
    def getCateoriesListByEventId(self, event_id:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT c.id as id,c.name as name from EventCategoryAssociation eca 
                    INNER JOIN Category c on c.id = eca.categoryId
                    WHERE eca.eventId = ?''', [event_id])
        value =cur.fetchall()
        cur.close()
        return list(map(lambda x:CategoryEntity.fromMap(x),value))    
             
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
        cur.execute('''UPDATE Event SET title = ?, description = ?, startDate = ?, endDate = ?, price = ?, address = ? WHERE id = ?''',
                         [event.title,event.description,event.startDate,event.endDate,event.price,event.address,event.id])
        cur.execute('DELETE FROM EventCategoryAssociation WHERE EventId = ?',[event.id])
        for categoryId in categoryIds:
            cur.execute('''INSERT INTO EventCategoryAssociation (categoryId,eventId) VALUES (?,?)''',[categoryId,event.id])
        cur.connection.commit()
        cur.close()           

    def getEventByIdWithTicketStatus(self,id:int,userId:int):
        current_date=datetime.now()
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.*,tp.TicketStatusId as ticketStatusId, ts.Name as ticketStatusName, 
                    (CASE WHEN (tp.id is null AND (e.startDate<=? AND e.endDate>=?)) THEN 1 ELSE 0 END) as canBuyTicket
                    from Event e 
                    LEFT JOIN TicketPayment tp on tp.eventId = e.Id AND tp.userId = ?
                    LEFT JOIN TicketStatus ts on ts.id = tp.ticketStatusId
                    WHERE e.id = ?  LIMIT 1''', [current_date,current_date,userId,id])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            raise Exception ("Event Not Found")
        return EventDetailEntity.fromMap(value)   
    
    def deleteEvent(self,id:int):    
        cur= self.databaseHelper.con.cursor()
        cur.execute('SELECT id FROM TicketPayment WHERE eventId=? LIMIT',[id])
        value =cur.fetchone()
        paymentExists= (value != None)  
        if(paymentExists):
            raise Exception("Cannot delete event, User has already applied for ticket for this event")
        cur.execute('DELETE FROM EventCategoryAssociation WHERE EventId = ?',[id])
        cur.execute('''DELETE Event WHERE id = ?''', [id])
        cur.connection.commit()
    
    # This retrieves all the events
    def getEventList(self)->list:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT * from Event''', )
        values =cur.fetchall()
        return list(map(lambda x:EventEntity.fromMap(x),values)) 
    
   
#    [currentDate]=None for admin
    def getFilteredEventList(self,currentDate,query:str,categoryId:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.* from Event e LEFT JOIN EventCategoryAssociation eca on eca.eventId = e.id WHERE '''
                    +str(("1" if currentDate is None else f''' e.endDate >='{str(currentDate)}''''')+' AND ')
                    +str("1" if categoryId is None else f''' eca.categoryId = {categoryId} ''')
                    +str("" if len(query.strip())==0 else f''' AND e.address Like '%{query.strip()}%' ''')
                    +''' GROUP BY e.id ORDER BY '''
                    +str(' e.endDate asc 'if currentDate is not None else ' e.id asc '))
        values =cur.fetchall()
        return list(map(lambda x:EventEntity.fromMap(x),values) )
    
    
#   validate if the [userId] can buy ticket of [eventId]        
    def allowToBuyTicket(self,userId:int,eventId:int)->bool:
        current_date=datetime.now()
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT (CASE WHEN (tp.id is null AND (e.startDate<=? AND e.endDate>=?)) THEN 1 ELSE 0 END) as canBuyTicket
                    from Event e 
                    LEFT JOIN TicketPayment tp on tp.eventId = e.Id AND tp.userId = ?
                    LEFT JOIN TicketStatus ts on ts.id = tp.ticketStatusId
                    WHERE e.id = ? LIMIT 1''', [current_date,current_date,userId,eventId])
        value =cur.fetchone()
        cur.close()
        if(value == None):
            return False
        return dict(value).get("canBuyTicket")==1
              
                      
   
 