

from datetime import datetime
from entity.event.event_detail_entity import EventDetailEntity
from services.database_helper import DatabaseHelper

from services.event_service import EventService


class TicketPaymentService:
    def __init__(self):
        self.databaseHelper=DatabaseHelper()
        self.eventService=EventService()
        
    def buyEventTicket(self,userId:int, eventId:int)->bool:
        if(self.__checkIfTicketPaymentExists(userId,eventId)):
            raise Exception("Ticket Already Bought for this event")
        if(not self.eventService.allowToBuyTicket(userId,eventId)):
            raise Exception("Cannot Buy ticket for this event")
        cur= self.databaseHelper.con.cursor()
        cur.execute('''INSERT INTO TicketPayment (ticketStatusId,eventId,userId) VALUES (?,?,?)''',[1,eventId,userId])
        cur.connection.commit()
        cur.close()
        
    def getUserTicketListWithEvent(self,userId:int)->list:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.*,tp.TicketStatusId as ticketStatusId, ts.Name as ticketStatusName, 0 as canBuyTicket
                    from TicketPayment tp 
                    INNER JOIN Event e on tp.eventId = e.Id AND tp.userId = ?
                    INNER JOIN TicketStatus ts on ts.id = tp.ticketStatusId
                    WHERE tp.userId = ?''', [userId,userId])
        values =cur.fetchall()
        cur.close()
        return list(map(lambda x:EventDetailEntity.fromMap(x),values ))  
     
    def getAllTicketListWithEvent(self)->list:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.*,tp.TicketStatusId as ticketStatusId, ts.Name as ticketStatusName, 0 as canBuyTicket
                    from TicketPayment tp 
                    INNER JOIN Event e on tp.eventId = e.Id
                    INNER JOIN TicketStatus ts on ts.id = tp.ticketStatusId
                    ''',)
        values =cur.fetchall()
        cur.close()
        return list(map(lambda x:EventDetailEntity.fromMap(x),values ))    
          
    def approveEventTicket(self,id:int)->bool:
        ticketInfo = self.getTicketPayementInfo()
        cur= self.databaseHelper.con.cursor()
        cur.execute('''UPDATE TicketPayment SET ticketStatusId=2 WHERE id = ?''',[id])
        cur.connection.commit()
        cur.close()

 
    def rejectEventTicket(self,id:int)->bool:
        ticketInfo = self.getTicketPayementInfo()
        cur= self.databaseHelper.con.cursor()
        cur.execute('''UPDATE TicketPayment SET ticketStatusId=3 WHERE id=?''',[id])
        cur.connection.commit()
        cur.close()

        
    def getTicketPayementInfo(self,id:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('SELECT * FROM TicketPayment WHERE id = ?',[id])
        cur.connection.commit()
        value =cur.fetchone()
        if(value == None):
            raise Exception("Payment information doesnot exists")
        
    def __checkIfTicketPaymentExists(self,userId:int, eventId:int)->bool:
        cur= self.databaseHelper.con.cursor()
        cur.execute('SELECT id FROM TicketPayment WHERE userId = ? AND eventId=?',[userId,eventId])
        cur.connection.commit()
        value =cur.fetchone()
        return (value != None)             
                      
   
 