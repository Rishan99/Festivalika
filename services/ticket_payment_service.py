

from services.database_helper import DatabaseHelper

from services.event_service import EventService


class TicketPaymentService:
    def __init__(self):
        self.databaseHelper=DatabaseHelper()
        self.eventService=EventService()
    
    def buyEventTicket(self,userId:int, eventId:int)->bool:
        try:
            if(self.eventService.allowToByTicket(eventId)):
                raise Exception("Cannot Buy ticket for this event")
            if(self.__checkIfTicketPaymentExists(userId,eventId)):
                raise Exception("Ticket Already Bought for this event")
            cur= self.databaseHelper.con.cursor()
            cur.execute('''INSERT INTO TicketPayment (TicketStatusId,EventId,UserId) VALUES (?,?,?)''',[1,eventId,userId])
            cur.close()
            return True
        except:
            return False
   
    def approveEventTicket(self,id:int)->bool:
        try:
            ticketInfo = self.getTicketPayementInfo()
            cur= self.databaseHelper.con.cursor()
            cur.execute('''UPDATE TicketPayment SET TicketStatusId=2 WHERE Id = ?''',[id])
            cur.close()
            return True
        except:
            return False
 
    def rejectEventTicket(self,id:int)->bool:
        try:
            ticketInfo = self.getTicketPayementInfo()
            cur= self.databaseHelper.con.cursor()
            cur.execute('''UPDATE TicketPayment SET TicketStatusId=3 WHERE Id=?''',[id])
            cur.close()
            return True
        except:
            return False  
        
    def getTicketPayementInfo(self,id:int):
        cur= self.databaseHelper.con.cursor()
        cur.execute('SELECT * FROM TicketPayment WHERE Id = ?',[id])
        value =cur.fetchone()
        if(value == None):
            raise Exception("Payment information doesnot exists")
        
    def __checkIfTicketPaymentExists(self,userId:int, eventId:int)->bool:
        cur= self.databaseHelper.con.cursor()
        cur.execute('SELECT Id FROM TicketPayment WHERE UserId = ? AND EventId=?',[userId,eventId])
        value =cur.fetchone()
        return (value != None)
              
                      
   
 