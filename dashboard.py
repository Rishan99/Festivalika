
from tkinter import *
from PIL import ImageTk,Image
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from entity.event.event_entity import EventEntity
import event_detail as ed
from services.event_service import EventService
from datetime import datetime
from services.general_service import GeneralService
import event_list as ud
from services.user_provider import UserProvider
from utility.assets import *


event_service = EventService()
general_service = GeneralService()

__root:Tk =None
__body_widget_frame:Frame=None
__selectedIndex:int = 0


def run():
    global __root,__body_widget_frame
    __root =Tk()
    app_drawer_frame=side_bar()
    # configuring _root
    app_drawer_frame.pack(side=LEFT,anchor='ne',fill='y',ipadx=45)
    body_frame=Frame(__root,bg='black',border=0)
    body_frame.pack(fill='both',side=RIGHT,expand=1)
    
    # configuring 
    body_frame.columnconfigure(0,weight=1)
    body_frame.columnconfigure(1,weight=1)
    body_frame.rowconfigure(0,weight=1)

    __body_widget_frame=Frame(body_frame,bg=backgroundColor)
    __body_widget_frame.grid(row=0,column=0,sticky='nwes',ipadx=200)

    bck_img = dashboard_img()
    background_label = Label(body_frame,image=bck_img)
    background_label.grid(row=0,column=1,sticky='news')
       
    
    # __root.resizable(0,0)
    # __root.state("zoomed")
    __root.geometry(f"{__root.winfo_screenwidth()}x{__root.winfo_screenheight()}")
    draw_body_widget()
    __root.mainloop()

def dashboard_img():
    bckImage=ImageTk.PhotoImage(Image.open(Dashboard_Background1).resize((396,1024),Image.LANCZOS))
    return bckImage
    


def side_bar()->Frame:
    app_drawer_frame = Frame(__root,bg=sideBarBackgroundColor,width=120)
    title_label=Label(app_drawer_frame,text=App_Name,font=('Arial',20,'bold'),fg="#6a3bff",bg=sideBarBackgroundColor,pady=30,padx=30)
    title_label.pack()
    menu_option_frame=Frame(app_drawer_frame,bg=sideBarBackgroundColor,)
    side_bar_title_style=('Poppins',12,'bold')
    event=Label(menu_option_frame,text='Event List',fg=sideBarTitleColor,bg=sideBarBackgroundColor,font=side_bar_title_style)
    event.bind('<Button-1>',lambda e,id=0: updateIndex(id))
    event.pack(pady=8)
    if(UserProvider().user.isAdmin):
        create_event=Label(menu_option_frame,text='Create Event',fg=sideBarTitleColor,bg=sideBarBackgroundColor,font=side_bar_title_style)
        create_event.pack()
        create_event.bind('<Button-1>',lambda e,id=1: updateIndex(id))
    
    my_ticket=Label(menu_option_frame,text= 'My Ticket List' if (not UserProvider().user.isAdmin) else 'Ticket List',fg=sideBarTitleColor,bg=sideBarBackgroundColor,font=side_bar_title_style,pady=10)
    my_ticket.bind('<Button-1>',lambda e,id=2: updateIndex(id))
    my_ticket.pack()
    
    if(UserProvider().user.isAdmin):
        user_list=Label(menu_option_frame,text='User List',fg=sideBarTitleColor,bg=sideBarBackgroundColor,font=side_bar_title_style,)
        user_list.bind('<Button-1>',lambda e,id=3: updateIndex(id))
        user_list.pack()

    Frame(menu_option_frame,bg=sideBarBackgroundColor).pack(fill='y',anchor='s',ipady=200)
    log_out=Label(menu_option_frame,text='Log Out',fg=sideBarTitleColor,bg=sideBarBackgroundColor,pady=10,font=side_bar_title_style)
    log_out.bind('<Button-1>',logout)
    log_out.pack()
    menu_option_frame.pack(expand=1,fill=BOTH)

    return app_drawer_frame
    
def logout(e):
    import authentication as auth
    __root.destroy()
    auth.loginPage() 

def draw_body_widget():
    global __selectedIndex
    childs = __body_widget_frame.winfo_children().copy()
    for child in childs:
        child.destroy()
    match __selectedIndex:
        case 0:
             ud.run(__body_widget_frame)  
        case 1:
            import create_event as ce
            ce.run(tk=__body_widget_frame) 
        case 2:
            import ticket_list as tl
            tl.run(tk=__body_widget_frame) 
        case 3:
            import user_list as ul
            ul.run(tk=__body_widget_frame)    
                                   
        
def updateIndex(i:int):
    global __selectedIndex
    if(__selectedIndex==i):return
    __selectedIndex=i   
    draw_body_widget() 
                                   
   
    
if(__name__=="__main__"):
    run()   