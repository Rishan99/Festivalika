
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from PIL import ImageTk,Image
from utility.assets import *
from entity.event.event_detail_entity import EventDetailEntity
from entity.event.event_entity import EventEntity
from services.auth_service import AuthService
from services.event_service import EventService
from datetime import datetime
from services.ticket_payment_service import TicketPaymentService
from services.user_provider import UserProvider
from utility.helper import error_message_box
from widgets.scrollable import  ScrollbarFrame


event_service = EventService()
ticket_service = TicketPaymentService()

__root:Toplevel =None
__event_id:int=None
__ticket_button:Widget=None
__event:EventDetailEntity=None



def run(id:int):
    global __root,__event_id
    __event_id=id
    __root=Toplevel()
    __configureBody()
    __root.mainloop()
    
def __configureBody():
    global __event,__event_id
    event_frame = Frame(master=__root,name='event_frame')
    __event=event_service.getEventByIdWithTicketStatus(__event_id,UserProvider().user.id)
    __root.title(__event.title)
    title_label=Label(event_frame,text=__event.title,font=('Arial',14),anchor="w")
    address_label=Label(event_frame,text=__event.address,font=('Arial',10,))
    status_text=__event.event_status_text()
    frame1 = Frame(master=event_frame)       
    status_label = Label(frame1,text=status_text,font=font.Font(weight="bold",size=10))
    price_label=Label(frame1,text="Price: "+str(__event.price),)
    description_label =Label(master=event_frame,text=__event.description)
    title_label.pack()
    address_label.pack()
    frame1.pack()
    status_label.pack(side=LEFT)
    price_label.pack(side=LEFT)
    description_label.pack()
    __ticket_status_widget(event_frame,)
    event_frame.pack()   

def __ticket_status_widget(master:Widget):
    if(UserProvider().user.isAdmin):
        return
    global __event,__ticket_button
    if(__event.canBuyTicket):
        __ticket_button =Button(master=master,text="Buy Ticket",command=__buy_ticket)
        __ticket_button.pack(side=BOTTOM)
    elif(__event.ticketStatusId is not None):
        __ticket_button = Label(master,text=f"Your Ticket Status is {__event.ticketStatusName}",font=font.Font(weight="bold",size=13))  
        __ticket_button.pack(side=BOTTOM) 
              
    
def __buy_ticket():
    try:
        ticket_service.buyEventTicket(UserProvider().user.id,__event_id)
        refresh_ticket_status()
    except BaseException as ex:
        error_message_box(str(ex))

def refresh_ticket_status():
    global __ticket_button,__event
    __ticket_button.destroy()
    __event=event_service.getEventByIdWithTicketStatus(__event_id,UserProvider().user.id)
    __ticket_status_widget(__root.winfo_children()[0])
            
        