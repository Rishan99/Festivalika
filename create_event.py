
from datetime import datetime
from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk,Image
from utility.assets import *
from entity.event.event_entity import EventEntity
from entity.user_entity import UserEntity
from utility.helper import convert_datetime_from_database, convert_datetime_to_default, error_message_box, success_message_box
from services.event_service import EventService
from services.general_service import GeneralService
from services.user_provider import UserProvider
from event_list import run
from tkcalendar import Calendar, DateEntry
from utility.validator import float_validator, empty_validator
eventService = EventService()
categoryList:list=GeneralService().getCategoryList()
# __root:Toplevel=None
event_id:int|None=None



def run(id:int|None=None,tk:Widget|None=None): 
    
    """ 
    Pass [id] if you want to update event, else pass as None to create a new event
    """
    global event_id,categoryList
    event_id=id
    global __root
    __root = tk if(tk is not None ) else Tk()
    title_var=StringVar(__root)
    price_var=DoubleVar(__root)
    address_var=StringVar(__root)
    start_date_var=StringVar(__root)
    end_date_var=StringVar(__root)
    event_detail_frame=LabelFrame(__root,bg="#d8d8d8",border=0)
    event_detail_frame.grid(row=0,column=0,ipady=90)

    # widgets inside frame
    Label(event_detail_frame,text="Create Event" if event_id is None else "Update Event",font=('Arial',"18","bold"),bg='#d8d8d8',fg="#6a3bff").grid(row=0,column=0,sticky='sw',padx=25,ipady=7)
    row =1
    placeTitle(event_detail_frame,"Title",row)
    row+=1
    title_entry=Entry(event_detail_frame,width=50,border=0,textvariable=title_var)
    defineEntryBoxPlace(row,title_entry)
    row+=1
    # 
    placeTitle(event_detail_frame,"Address",row)
    row+=1
    address_entry=Entry(event_detail_frame,width=50,border=0,textvariable=address_var)
    defineEntryBoxPlace(row,address_entry)
    row+=1
    # 
    placeTitle(event_detail_frame,"Price",row) 
    row+=1   
    # __root.register to register the function callback for the widget
    price_entry=Entry(event_detail_frame,width=50,border=0,validate='all',validatecommand=(__root.register(float_validator),'%P'),textvariable=price_var)
    defineEntryBoxPlace(row,price_entry)
    row+=1
    # 
    placeTitle(event_detail_frame,"Start Date",row)
    row+=1
    start_date_entry= DateEntry(event_detail_frame,width=47,textvariable=start_date_var)
    defineEntryBoxPlace(row,start_date_entry)
    row+=1
    # 
    placeTitle(event_detail_frame,"End Date",row)
    row+=1
    end_date_entry = DateEntry(event_detail_frame,width=47,textvariable=end_date_var)
    defineEntryBoxPlace(row,end_date_entry)
    row+=1
    #  
    placeTitle(event_detail_frame,"Categories",row)
    row+=1
    list_box:Listbox=None
    if(len(categoryList)>0):
        category_list_frame=Frame(event_detail_frame)
        scrollbar = Scrollbar(category_list_frame)
        list_box=Listbox(category_list_frame,selectmode=MULTIPLE,width=50,height=4,)
        scrollbar.pack(side = RIGHT, fill = BOTH)
        list_box.pack(side = LEFT, fill = BOTH)
        list_box.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = list_box.yview)
        for c in range(len(categoryList)):
            list_box.insert(c,categoryList[c].name)
        defineEntryBoxPlace(row,category_list_frame)
        row+=3
    # 
    placeTitle(event_detail_frame,"Description",1,1)
    description_entry=Text(event_detail_frame,width=50,border=0,)
    description_entry.grid(row=2,column=1,sticky='nw',padx=25,ipady=8,rowspan=10,columnspan=1)
    # 
    loginButton=Button(event_detail_frame,text="Create Event" if event_id is None else "Update Event",fg="white",bg="#6a3bff",command=lambda :
        __create_or_update_event(title_entry.get(),address_entry.get(),price_entry.get(),description_entry.get("0.0",END),
                                 start_date_entry.get(),end_date_entry.get(),list(map(lambda x:next(filter(lambda z:z.name == list_box.get(x),categoryList)).id,
                                 list_box.curselection()))))
    loginButton.grid(row=row,column=0,columnspan=2,sticky="s",ipady=8,pady=15,ipadx=60)
    
    # Getting details of event Id is event Id is not null, means that this GUI is for upadting event
    if(event_id is not None):
        event_detail:EventEntity=eventService.getEventById(event_id)
        selected_categories:list=eventService.getCateoriesListByEventId(event_id)
        for cat in selected_categories:
            try:
                list_box.select_set(list(list_box.get(0,END)).index(cat.name))
            except:
                pass    
        title_var.set(event_detail.title)  
        description_entry.insert("0.0",event_detail.description)
        price_var.set(event_detail.price)  
        address_var.set(event_detail.address)  
        start_date_var.set(convert_datetime_to_default(convert_datetime_from_database(event_detail.startDate))) 
        end_date_var.set(convert_datetime_to_default(convert_datetime_from_database(event_detail.endDate))) 
        
    __root.mainloop()

    
def __create_or_update_event(title:str,address:str,price:str,description:str,start_date:str,end_date:str,category_list:list):
    try:
        entity=EventEntity(event_id,title,address,description,str(start_date),str(end_date),(price),"" )
        is_validation_success=__validate_data(entity) 
        if(event_id is None):
            eventService.addEvent(entity,category_list)
            success_message_box("Event has been added")
        else:
            eventService.updateEvent(entity,category_list)
            success_message_box("Event has been updated")
    except BaseException as ex:
        error_message_box(str(ex)) 


def __validate_data( entity:EventEntity):
    entity.description=entity.description.removesuffix('\n')
    if(empty_validator(entity.title) or empty_validator(entity.address) or empty_validator(str(entity.price))):
        raise Exception("One or more field is empty")
    if (not float_validator(str(entity.price))):
        raise Exception("Error, Invalid price")
    if(empty_validator(entity.startDate) or empty_validator(entity.endDate)):
        raise Exception("Start Date or End Date cannot be empty")  
    try:
        entity.startDate=datetime.strptime(entity.startDate,"%m/%d/%y")
        entity.endDate=datetime.strptime(entity.endDate,"%m/%d/%y")
        if(entity.startDate>entity.endDate):
            raise Exception("Start Date must be less than or equal to End Date")
    except ValueError:    
        raise Exception("Invalid Start Date or End Date") 
    return True
    
def placeTitle(master:Widget,title:str,row:int,col:int|None=0):
    Label(master,text=title,font=('Arial',10,'bold'),bg="#d8d8d8").grid(row=row,column=col,sticky='w',padx=25)
      
    
def defineEntryBoxPlace(row:int,widget:Widget,col:int|None=0):
    widget.grid(row=row,column=col,sticky='nw',padx=25,ipady=8,)
    
# if(__name__=="__main__"):    
#     run()
  