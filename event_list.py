
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from entity.event.event_entity import EventEntity
import event_detail as ed
from services.event_service import EventService
from datetime import datetime
from services.general_service import GeneralService
from services.user_provider import UserProvider
from utility.helper import error_message_box
from widgets.scrollable import  ScrollbarFrame
from utility.assets import *

event_service = EventService()
general_service = GeneralService()
category_list=general_service.getCategoryList()
__root:Toplevel =None
__event_list_data_frame:Frame=None
dropdown_options = [
]   
selectedCategory=None
categoryVar=None


def run(frame:Widget):
    global __root,dropdown_options,categoryVar,__event_list_data_frame
    __root =frame
    __event_list_data_frame=Frame(__root,width=22)
    # __root.title(str(UserProvider().user.isAdmin))
    dropdown_options=list(map(lambda x:x.name,category_list))
    dropdown_options.insert(0,"All")
    categoryVar= StringVar(__root,value=dropdown_options[0])
    __event_heading()
    __showDropDown()
    __show_event_list()
    __event_list_data_frame.pack(expand=1,fill='both')


def __showDropDown():
    dropdown_menu = OptionMenu(__root,categoryVar, *dropdown_options,command=__onOptionSelect ) 
    dropdown_menu.pack()     
    
def __onOptionSelect(value):
    global selectedCategory
    try:
        index=(dropdown_options.index(value)) 
        if(index==0):
            selectedCategory=None
        else:
            selectedCategory= category_list[dropdown_options.index(value)-1].id     
    except ValueError:
        selectedCategory=None    
    __refresh_event_list()       
    
def __event_heading():
    Label(__root,text="Events For You",font=font.Font(weight="bold",size=16),bg=backgroundColor).pack()    
    
def __refresh_event_list():
    global __event_list_data_frame
    childs = __event_list_data_frame.children.copy()
    for child in childs.values():
        child.destroy()
    __show_event_list()

def __on_event_pressed(event_id:int):
    ed.run(event_id)

def __show_event_list():
    event_list=event_service.getFilteredEventList(datetime.now() if  not UserProvider().user.isAdmin else None,"",selectedCategory)
    if(len(event_list)==0):
        Label(__event_list_data_frame,text="No Events Found",font=font.Font(weight="normal",size=14,)).pack(fill=BOTH,expand=1,padx=80,pady=80)
    else:    
        __scrollable_body = ScrollbarFrame(__event_list_data_frame,)
        __scrollable_body.pack(fill='both',expand=1, anchor='e')
        event_list_frame=__scrollable_body.scrolled_frame
        for event in event_list:
            event_frame = Frame(event_list_frame)
            widget=__event_widget(event_frame,event)
            event_frame.bind("<Button-1>",lambda event, id=event.id: __on_event_pressed(id))
            widget.pack(anchor="w",padx=10)
            separator = Separator(event_frame, orient='horizontal')
            separator.pack(fill='x',expand=1,pady=5,padx=10,)
            event_frame.pack(fill='x',expand=1,anchor='w')
    
    #   change layout here
def __event_widget(master,event: EventEntity)->Widget:
    event_frame = Frame(master=master)
    title_label=Label(event_frame,text=event.title,font=('Poppins',14,'bold'),anchor="w")
    address_label=Label(event_frame,text="Venue: "+event.address,font=('Poppins',10,'bold'))
    status_text=event.event_status_text()     
    status_label = Label(event_frame,text=status_text,font=('Poppins',10,'bold'))
    row=0
    title_label.grid(row=row,column=0,sticky="w")
    row+=1
    address_label.grid(row=row,column=0,sticky="w")
    row+=1
    status_label.grid(row=row,column=0,sticky="w")
    row+=1
    if(len(event.description)>0):
        description_label =Label(master=event_frame,text=event.description)
        description_label.grid(row=row,column=0,sticky="w")
        row+=1
    if(UserProvider().user.isAdmin):
        Button(event_frame,text="Delete Event",command=lambda id = event.id:delete_event(id)).grid(row=row,column=0,sticky="w")
        
        
    return event_frame

def delete_event(eventId:int):
    response=mb.askyesno(title='Confirm',message="Are you sure you want to delete this event?")
    if(response):
        try:
            event_service.deleteEvent(eventId)
            __refresh_event_list()
        except BaseException as ex:
            error_message_box(str(ex))
