
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
from main import userId
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
    event:EventDetailEntity=event_service.getEventByIdWithTicketStatus(userId,_event_id__)
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
        ticket_service.buyEventTicket(userId,_event_id__)
    except BaseException as ex:
        mb.showerror(title="Error",message=str(ex))
            
        
# def event_heading():
#     Label(__root,text="Events For You",font=font.Font(weight="bold",size=16)).pack()    
    
# def refresh_event_list():
#     childs = __root.children.copy()
#     for child in childs.values():
#         child.destroy()
#     event_heading()    
#     __show_event_list()
    
# def __show_event_list():
#     event_list=event_service.getEventListForUser('2022-01-15')
#     if(len(event_list)==0):
#         Label(__root,text="No Events Found",font=font.Font(weight="normal",size=14,)).pack(fill=BOTH,expand=1,padx=20,pady=20)
#     else:    
#         __scrollable_body = ScrollbarFrame(__root,)
#         __scrollable_body.pack(fill='both',expand=1, anchor='e')
#         event_list_frame=__scrollable_body.scrolled_frame
#         for event in event_list:
#             event_frame = Frame(event_list_frame)
#             widget=__event_widget(event_frame,event)
#             widget.pack(anchor="w",padx=10)
#             separator = Separator(event_frame, orient='horizontal')
#             separator.pack(fill='x',expand=1,pady=5,padx=10,)
#             event_frame.pack(fill='x',expand=1,anchor='w')
    
      
# def __event_widget(master,event: EventEntity)->Widget:
#     has_event_started=False
#     has_event_ended=False
#     start_date=datetime.strptime(event.startDate,"%Y-%m-%d")
#     end_date=datetime.strptime(event.endDate,"%Y-%m-%d")
#     current_datetime= datetime.now()
#     if(current_datetime>=start_date):
#         has_event_started=True
#     if(current_datetime>end_date):
#         has_event_ended=True
        
#     event_frame = Frame(master=master)
#     title_label=Label(event_frame,text=event.title,font=('Arial',14),anchor="w")
#     address_label=Label(event_frame,text=event.address,font=('Arial',10,))
#     status_text:str|None
#     if(not has_event_started):
#         status_text = f"Event starts in {(start_date - current_datetime).days} days"
#     elif(has_event_started and not has_event_ended):
#         if(current_datetime==end_date):
#             status_text = f"Event Ends Today" 
#         else:
#             status_text = f"Event Ends in {(end_date - current_datetime).days} days"       
#     else:    
#         status_text = f"Event Ended {(current_datetime - end_date).days} days ago"   
#     frame1 = Frame(master=event_frame)       
#     status_label = Label(frame1,text=status_text,font=font.Font(weight="bold",size=10))
#     price_label=Label(frame1,text="Price: "+str(event.price),)
#     description_label =Label(master=event_frame,text=event.description)
#     title_label.grid(row=0,column=0,sticky="w")
#     address_label.grid(row=1,column=0,sticky="w")
#     frame1.grid(row=2,column=0,sticky="w")
#     status_label.pack(side=LEFT)
#     price_label.pack(side=LEFT)
#     description_label.grid(row=3,column=0,sticky="w")
#     return event_frame
    
# if(__name__=="__main__"):
#     runUserDashboard()   