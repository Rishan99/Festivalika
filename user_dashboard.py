
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from PIL import ImageTk,Image
from assets import *
from entity.event.event_entity import EventEntity
from services.auth_service import AuthService
from services.event_service import EventService
from datetime import datetime


event_service = EventService()

root:Toplevel =None

def runUserDashboard():
    global root
    root=Toplevel()
    root.title("ddd")
    event_list=event_service.getEventListForUser(datetime.now().isoformat(sep='T').split('T')[0])
    for event in event_list:
        widget=event_widget(root,event)
        widget.pack(anchor="w")
        separator = Separator(root, orient='horizontal')
        separator.pack(fill='x',pady=5)
        
    root.mainloop()
    
    
      
def event_widget(master,event: EventEntity)->Widget:
    has_event_started=False
    has_event_ended=False
    start_date=datetime.strptime(event.startDate,"%Y-%m-%d")
    end_date=datetime.strptime(event.endDate,"%Y-%m-%d")
    current_datetime= datetime.now()
    if(current_datetime>=start_date):
        has_event_started=True
    if(current_datetime>end_date):
        has_event_ended=True
        
    event_frame = Frame(master=master)
    title_label=Label(event_frame,text=event.title,font=('Arial',14),anchor="w")
    address_label=Label(event_frame,text=event.address,font=('Arial',10,))
    status_text:str|None
    if(not has_event_started):
        status_text = f"Event starts in {(start_date - current_datetime).days} days"
    elif(has_event_started and not has_event_ended):
        if(current_datetime==end_date):
            status_text = f"Event Ends Today" 
        else:
            status_text = f"Event Ends in {(end_date - current_datetime).days} days"       
    else:    
        status_text = f"Event Ended {(end_date - current_datetime).days} days ago"   
    frame1 = Frame(master=event_frame)       
    status_label = Label(frame1,text=status_text,font=font.Font(weight="bold",size=10))
    price_label=Label(frame1,text="Price: "+str(event.price),)
    description_label =Label(master=event_frame,text=event.description)
    title_label.grid(row=0,column=0,sticky="w")
    address_label.grid(row=1,column=0,sticky="w")
    frame1.grid(row=2,column=0,sticky="w")
    status_label.pack(side=LEFT)
    price_label.pack(side=LEFT)
    description_label.grid(row=3,column=0,sticky="w")
    return event_frame
    
if(__name__=="__main__"):
    runUserDashboard()    