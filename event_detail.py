
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from PIL import ImageTk,Image
from assets import *
from entity.event.event_detail_entity import EventDetailEntity
from entity.event.event_entity import EventEntity
from services.auth_service import AuthService
from services.event_service import EventService
from datetime import datetime
from services.ticket_payment_service import TicketPaymentService
from services.user_provider import UserProvider
from widgets.scrollable import  ScrollbarFrame


event_service = EventService()
ticket_service = TicketPaymentService()

__root:Toplevel =None
_event_id__:int=None



def runEventDetail(id:int):
    global __root,_event_id__
    _event_id__=id
    __root=Toplevel()
    __configureBody()
    __root.mainloop()
    
def __configureBody():

    event_frame = Frame(master=__root)
    event:EventDetailEntity=event_service.getEventByIdWithTicketStatus(UserProvider().user.id,_event_id__)
    __root.title(event.title)
    title_label=Label(event_frame,text=event.title,font=('Arial',14),anchor="w")
    address_label=Label(event_frame,text=event.address,font=('Arial',10,))
    status_text=event.event_status_text()
    frame1 = Frame(master=event_frame)       
    status_label = Label(frame1,text=status_text,font=font.Font(weight="bold",size=10))
    price_label=Label(frame1,text="Price: "+str(event.price),)
    description_label =Label(master=event_frame,text=event.description)
    title_label.pack()
    address_label.pack()
    frame1.pack()
    status_label.pack(side=LEFT)
    price_label.pack(side=LEFT)
    description_label.pack()
    if(event.canBuyTicket):
        ticket_button =Button(master=event_frame,text="Buy Ticket",command=__buy_ticket)
        ticket_button.pack(side=BOTTOM)
    elif(event.ticketStatusId is not None):
        ticket_status_label = Label(event_frame,text=f"Your Ticket Status is {event.ticketStatusName}",font=font.Font(weight="bold",size=13))  
        ticket_status_label.pack(side=BOTTOM)  
    event_frame.pack()         
    
def __buy_ticket():
    try:
        ticket_service.buyEventTicket(UserProvider().user.id,_event_id__)
    except BaseException as ex:
        mb.showerror(title="Error",message=str(ex))
            
        