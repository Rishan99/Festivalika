
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from PIL import ImageTk,Image
from assets import *
from entity.event.event_entity import EventEntity
from event_detail import runEventDetail
from services.auth_service import AuthService
from services.event_service import EventService
from datetime import datetime
from services.general_service import GeneralService

from widgets.scrollable import  ScrollbarFrame


event_service = EventService()
general_service = GeneralService()

__root:Toplevel =Tk()
# __event_list_data_frame=Frame(__root,width=9999)
dropdown_options = [
]   
selectedCategory=None
categoryVar = StringVar(value="Select a category")


def runUserDashboard():
    global __root,dropdown_options,__event_list_data_frame,main_dashboard_frame
    __root.title("Festivalika")
    __root.geometry("800x500")

    # configuring _root
    __root.columnconfigure(0,weight=1)
    __root.columnconfigure(1,weight=1)
    __root.columnconfigure(2,weight=1)
    __root.rowconfigure(0,weight=1)



    
    # frame
    main_dashboard_frame=LabelFrame(__root)
    main_dashboard_frame.grid(row=0,column=2,sticky="news")
    __event_list_data_frame=LabelFrame(main_dashboard_frame,bg="#ffffff")
    __event_list_data_frame.grid(row=0,column=1,sticky="news")
    app_drawer_frame=LabelFrame(__root,bg="#091924")
    app_drawer_frame.grid(row=0,column=0,sticky="news")

    # configuring main_dashboard_frame
    main_dashboard_frame.columnconfigure(0,weight=1)
    main_dashboard_frame.columnconfigure(1,weight=1)
    main_dashboard_frame.rowconfigure(0,weight=1)

    # configuring app_drawer_frame using grid
    app_drawer_frame.columnconfigure(0,weight=1)
    # app_drawer_frame.columnconfigure(1,weight=1)
    app_drawer_frame.rowconfigure(0,weight=1)
    app_drawer_frame.rowconfigure(1,weight=1)
    app_drawer_frame.rowconfigure(2,weight=1)
    app_drawer_frame.rowconfigure(3,weight=1)
    app_drawer_frame.rowconfigure(4,weight=1)
    app_drawer_frame.rowconfigure(5,weight=1)
    app_drawer_frame.rowconfigure(6,weight=1)
    app_drawer_frame.rowconfigure(7,weight=1)

    # making labels for app_drawer_frame
    festi=Label(app_drawer_frame,text="Festivalika",font=('Arial',10,'bold'),bg="#091924",fg="#f3f6f4")
    festi.grid(row=1,column=0,sticky='w')
    event=Button(app_drawer_frame,text="Event",font=('Arial',10,'bold'),bg="#091924",fg="#f3f6f4")
    event.grid(row=3,column=0,sticky='w')
    my_tick=Button(app_drawer_frame,text="My Ticket",font=('Arial',10,'bold'),bg="#091924",fg="#f3f6f4")
    my_tick.grid(row=4,column=0,sticky='w')
    account=Button(app_drawer_frame,text="My Account",font=('Arial',10,'bold'),bg="#091924",fg="#f3f6f4")
    account.grid(row=5,column=0,sticky='w')
    l_out=Button(app_drawer_frame,text="Log Out",font=('Arial',10,'bold'),bg="#091924",fg="#f3f6f4")
    l_out.grid(row=7,column=0,sticky='ws')

    dropdown_options=list(map(lambda x:x.name,general_service.getCategoryList()))
    # __event_heading()
    # __showDropDown()
    # __show_event_list()
    # __event_list_data_frame.pack(expand=1,fill='both')
    __root.mainloop()


def image_insert():
    img=Image.open(Dashboard_Background1)
    resize=img.resize((400,600),Image.LANCZOS)
    nimg=ImageTk.PhotoImage(resize)
    label=Label(__root,image=nimg)
    label.grid(row=0,column=0,columnspan=2)

def __showDropDown():
    dropdown_menu = OptionMenu(__event_list_data_frame,categoryVar, *dropdown_options,command=lambda x:__onOptionSelect(x) ) 
    dropdown_menu.pack()     
    
def __onOptionSelect(value):
    global selectedCategory
    selectedCategory=(dropdown_options.index(value)) 
    refresh_event_list()       
    
def __event_heading():
    Label(__event_list_data_frame,text="Events For You",font=font.Font(weight="bold",size=16)).pack()    
    
def refresh_event_list():
    childs = __event_list_data_frame.children.copy()
    for child in childs.values():
        child.destroy()
    __show_event_list()

def __on_event_pressed(event_id:int):
    runEventDetail(event_id)

def __show_event_list():
    event_list=event_service.getFilteredEventList(datetime.now(),"",selectedCategory)
    if(len(event_list)==0):
        Label(__event_list_data_frame,text="No Events Found",font=font.Font(weight="normal",size=14,)).pack(fill=BOTH,expand=1,padx=20,pady=20)
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
    
      
def __event_widget(master,event: EventEntity)->Widget:
    event_frame = Frame(master=master)
    title_label=Label(event_frame,text=event.title,font=('Arial',14),anchor="w")
    address_label=Label(event_frame,text=event.address,font=('Arial',10,))
    status_text=event.event_status_text()
    app_drawer_frame = Frame(master=event_frame)       
    status_label = Label(app_drawer_frame,text=status_text,font=font.Font(weight="bold",size=10))
    price_label=Label(app_drawer_frame,text="Price: "+str(event.price),)
    description_label =Label(master=event_frame,text=event.description)
    title_label.grid(row=0,column=0,sticky="w")
    address_label.grid(row=1,column=0,sticky="w")
    app_drawer_frame.grid(row=2,column=0,sticky="w")
    status_label.pack(side=LEFT)
    price_label.pack(side=LEFT)
    description_label.grid(row=3,column=0,sticky="w")
    return event_frame
    
if(__name__=="__main__"):
    runUserDashboard()   