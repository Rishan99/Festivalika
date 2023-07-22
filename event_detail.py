
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
    # __root.mainloop()
    
def __configureBody():
    global __event,__event_id
    event_frame = Frame(master=__root,name='event_frame')
    __event=event_service.getEventByIdWithTicketStatus(__event_id,UserProvider().user.id)
    __root.title(__event.title)
    event_detail=Label(event_frame,text="Event Details",font=('Poppins',14))
    event_detail.grid(row=0,column=0,sticky='w')
    title_label=Label(event_frame,text="Event Name: "+__event.title,font=('Poppins',8,'bold'),anchor="w")
    address_label=Label(event_frame,text="Venue: "+__event.address,font=('Poppins',8,'bold'))
    status_text=__event.event_status_text()
    frame1 = Frame(master=event_frame)       
    status_label = Label(frame1,text=status_text,font=font.Font(weight="bold",size=9))
    price_label=Label(frame1,text="Price: "+str(__event.price),font=('Poppins',8,'bold'))
    description_label =Label(master=event_frame,text=__event.description)
    title_label.grid(column=0,row=1,sticky='w')
    address_label.grid(column=0,row=2,sticky='w')
    frame1.grid(column=0,row=3,sticky='w')
    status_label.grid(column=0,row=0,sticky='w')
    price_label.grid(column=0,row=1,sticky='w')
    description_label.grid(column=0,row=4,sticky='w')
    __ticket_status_widget(event_frame,)
    event_frame.pack()   

def __ticket_status_widget(master:Widget):
    if(UserProvider().user.isAdmin):
        return
    global __event,__ticket_button
    if(__event.canBuyTicket):
        __ticket_button =Button(master=master,text="Buy Ticket",command=__buy_ticket,bg=primaryColor,font=('Poppins',8,'bold'))
        __ticket_button.grid(column=0,row=5)
    elif(__event.ticketStatusId is not None):
        __ticket_button = Label(master,text=f"Your Ticket Status is {__event.ticketStatusName}",font=font.Font(weight="bold",size=12))  
        __ticket_button.grid(column=0,row=5) 
              
    
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
            
        