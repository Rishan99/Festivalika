

from datetime import datetime
from entity.event.event_detail_entity import EventDetailEntity
from entity.ticket_payment_entity import TicketPaymentEntity
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
        
    def getUserTicketList(self,userId:int)->list:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.id as eventId, e.title as eventTitle, tp.id, tp.ticketStatusId, ts.name as ticketStatus, tp.userId, u.name, tp.createdDate
                    from TicketPayment tp 
                    INNER JOIN Event e on tp.eventId = e.Id
                    INNER JOIN TicketStatus ts on ts.id = tp.ticketStatusId
                    INNER JOIN User u on u.id = tp.userId
                    WHERE tp.userId = ?''', [userId])
        values =cur.fetchall()
        cur.close()
        return list(map(lambda x:TicketPaymentEntity.fromMap(x),values ))  
     
    def getAllTicketList(self)->list:
        cur= self.databaseHelper.con.cursor()
        cur.execute('''SELECT e.id as eventId, e.title as eventTitle, tp.id, tp.ticketStatusId, ts.name as ticketStatus, tp.userId, u.name as userName, tp.createdDate
                    from TicketPayment tp 
                    INNER JOIN Event e on tp.eventId = e.Id
                    INNER JOIN TicketStatus ts on ts.id = tp.ticketStatusId
                    INNER JOIN User u on u.id = tp.userId
                    ''',)
        values =cur.fetchall()
        cur.close()
        return list(map(lambda x:TicketPaymentEntity.fromMap(x),values ))    
          
    def approveEventTicket(self,id:int)->bool:
        ticketInfo = self.getTicketPayementInfo(id)
        cur= self.databaseHelper.con.cursor()
        cur.execute('''UPDATE TicketPayment SET ticketStatusId=2 WHERE id = ?''',[id])
        cur.connection.commit()
        cur.close()
        return True

 
    def rejectEventTicket(self,id:int)->bool:
        ticketInfo = self.getTicketPayementInfo(id)
        cur= self.databaseHelper.con.cursor()
        cur.execute('''UPDATE TicketPayment SET ticketStatusId=3 WHERE id=?''',[id])
        cur.connection.commit()
        cur.close()
        return True
        
    def deleteEventTicket(self,id:int)->bool:
        ticketInfo = self.getTicketPayementInfo(id)
        if(dict(ticketInfo).get('ticketStatusId')==2):
            raise BaseException ("Approved Ticket cannot be deleted")
        cur= self.databaseHelper.con.cursor()
        cur.execute('''DELETE FROM TicketPayment WHERE id=?''',[id])
        cur.connection.commit()
        cur.close()
        return True
        
    def getTicketPayementInfo(self,id:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('SELECT * FROM TicketPayment WHERE id = ?',[id])
        value =cur.fetchone()
        if(value == None):
            raise Exception("Payment information doesnot exists")
        return value
  
        
    def __checkIfTicketPaymentExists(self,userId:int, eventId:int)->bool:
        cur= self.databaseHelper.con.cursor()
        cur.execute('SELECT id FROM TicketPayment WHERE userId = ? AND eventId=?',[userId,eventId])
        value =cur.fetchone()
        return (value != None)             
                      
   
 