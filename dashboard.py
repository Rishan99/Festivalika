
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
__body_frame:Frame=None
__selectedIndex:int = 0


def run():
    global __root,__body_frame,event_picture_frame,background_label
    __root =Tk()
    app_drawer_frame=side_bar()
    # configuring _root
    app_drawer_frame.pack(side=LEFT,anchor='ne',fill='y',ipadx=45)
    event_picture_frame=Frame(__root,bg='black',border=0)
    event_picture_frame.pack(fill='both',side=RIGHT,expand=1)
    # configuring reg
    event_picture_frame.columnconfigure(0,weight=1)
    event_picture_frame.rowconfigure(0,weight=1)
    
    bck_img = dashboard_img()
    background_label = Label(event_picture_frame,image=bck_img)
    background_label.grid(row=0,column=1)
                           
    __body_frame=Frame(event_picture_frame,bg="#ffffff")
    __body_frame.grid(row=0,column=0,sticky='nws',ipadx=100)
    __root.resizable(0,0)
    __root.state("zoomed")
    __root.geometry(f"{__root.winfo_screenwidth()}x{__root.winfo_screenheight()}")
    draw_side_bar()
    __root.mainloop()

def dashboard_img():
    bckImage=ImageTk.PhotoImage(Image.open(Dashboard_Background1).resize((396,1024),Image.LANCZOS))
    return bckImage
    


def side_bar()->Frame:
    app_drawer_frame = Frame(__root,bg="#091924",width=120)

    # # configuring app_drawer_frame
    # app_drawer_frame.columnconfigure(0,weight=1)
    # app_drawer_frame.rowconfigure((tuple(range(20))),weight=1)


    festi=Label(app_drawer_frame,text="Festivalika",font=('Arial',20,'bold'),fg="#6a3bff",bg="#091924",pady=30,padx=30)
    festi.pack()

    menu_option_frame=Frame(app_drawer_frame,bg="#091924",)


    event=Label(menu_option_frame,text='Event List',fg="#ffffff",bg="#091924",font=('Poppins',12,'bold'))
    event.bind('<Button-1>',lambda e,id=0: updateIndex(id))
    event.pack()
    if(UserProvider().user.isAdmin):
        create_event=Label(menu_option_frame,text='Create Event',fg='#ffffff',bg="#091924",pady=10,font=('Poppins',12,'bold'))
        create_event.pack()
        create_event.bind('<Button-1>',lambda e,id=1: updateIndex(id))
    
    my_ticket=Label(menu_option_frame,text= 'My Ticket List' if (not UserProvider().user.isAdmin) else 'Ticket List',fg='#ffffff',bg="#091924",font=('Poppins',12,'bold'),pady=10)
    my_ticket.bind('<Button-1>',lambda e,id=2: updateIndex(id))
    my_ticket.pack()
    
    if(UserProvider().user.isAdmin):
        user_list=Label(menu_option_frame,text='User List',fg='#ffffff',bg="#091924",font=('Poppins',12,'bold'),pady=10)
        user_list.bind('<Button-1>',lambda e,id=3: updateIndex(id))
        user_list.pack()

    Frame(menu_option_frame,bg="#091924").pack(expand=1,fill='y',anchor='s',)
    log_out=Label(menu_option_frame,text='Log Out',fg='#ffffff',bg="#091924",pady=10)
    log_out.bind('<Button-1>',logout)
    log_out.pack()
    menu_option_frame.pack(expand=1,fill=BOTH)

    return app_drawer_frame
    
def logout(e):
    import authentication as auth
    __root.destroy()
    auth.loginPage() 

def draw_side_bar():
    global __selectedIndex
    childs = __body_frame.winfo_children().copy()
    for child in childs:
        child.destroy()
    match __selectedIndex:
        case 0:
             ud.run(__body_frame)  
        case 1:
            import create_event as ce
            ce.run(tk=__body_frame) 
        case 2:
            import ticket_list as tl
            tl.run(tk=__body_frame) 
        case 3:
            import user_list as ul
            ul.run(tk=__body_frame)    
                                   
        
def updateIndex(i:int):
    global __selectedIndex
    if(__selectedIndex==i):return
    __selectedIndex=i   
    draw_side_bar() 
                                   
   
    
if(__name__=="__main__"):
    run()   