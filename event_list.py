
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
    global __root,dropdown_options,categoryVar,__event_list_data_frame,selectedCategory
    __root =frame
    __root.config(bg=backgroundColor)
    __event_list_data_frame=Frame(__root,width=22)
    dropdown_options=list(map(lambda x:x.name,category_list))
    dropdown_options.insert(0,"All")
    selectedCategory=None
    categoryVar= StringVar(__event_list_data_frame,value=dropdown_options[0])
    __event_heading()
    __showDropDown()
    __show_event_list()
    __event_list_data_frame.pack(expand=1,fill='both')


def __showDropDown():
    dropdown_menu = OptionMenu(__root,categoryVar, *dropdown_options,command=__onOptionSelect ) 
    dropdown_menu.config(bg=dropdowncolor,font=('Poppins',8,'bold'))
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
        Label(__event_list_data_frame,text="No Events Found",font=font.Font(weight="normal",size=14,),bg=backgroundColor).pack(fill=BOTH,expand=1,ipadx=120,ipady=80)
    else:    
        __scrollable_body = ScrollbarFrame(__event_list_data_frame)
        __scrollable_body.pack(fill='both',expand=1, anchor='e')
        event_list_frame=__scrollable_body.scrolled_frame
       
        for event in event_list:
            # event_frame = Frame(event_list_frame,bg=backgroundColor)
            event_frame=__event_widget(event_list_frame,event,)
            event_frame.bind("<Button-1>",lambda event, id=event.id: __on_event_pressed(id))
            event_frame.pack(expand=1,anchor='w',fill='x')
            Frame(event_list_frame,height=10,width=9999).pack(expand=1,fill=Y)
    
    #   change layout here
def __event_widget(master,event: EventEntity)->Widget:
    event_frame = Frame(master=master,bg=backgroundColor,padx=10,pady=10)
    event_frame.bind("<Button-1>",lambda event, id=event.id: __on_event_pressed(id))
    title_label=Label(event_frame,text=event.title,font=('Poppins',14,'bold'),anchor="w",bg=backgroundColor)
    title_label.bind("<Button-1>",lambda event, id=event.id: __on_event_pressed(id))
    address_label=Label(event_frame,text="Venue: "+event.address,font=('Poppins',10,'bold'),bg=backgroundColor)
    address_label.bind("<Button-1>",lambda event, id=event.id: __on_event_pressed(id))
    status_text=event.event_status_text()     
    status_label = Label(event_frame,text=status_text,font=('Poppins',10,'bold'),bg=backgroundColor)
    status_label.bind("<Button-1>",lambda event, id=event.id: __on_event_pressed(id))
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
        buttom_frame = Frame(event_frame,bg=backgroundColor,)
        buttom_frame.grid(row=row,column=0,sticky="w")
        Button(buttom_frame,text="Edit Event",command=lambda id = event.id:edit_event(id)).pack(side=LEFT)
        Button(buttom_frame,text="Delete Event",command=lambda id = event.id:delete_event(id)).pack(side=RIGHT,padx=8)
    

    return event_frame

def edit_event(eventId:int):
    import create_event as ce
    ce.run(eventId,callback=lambda :__refresh_event_list())

def delete_event(eventId:int):
    response=mb.askyesno(title='Confirm',message="Are you sure you want to delete this event?")
    if(response):
        try:
            event_service.deleteEvent(eventId)
            __refresh_event_list()
        except BaseException as ex:
            error_message_box(str(ex))
