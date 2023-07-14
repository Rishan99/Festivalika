
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from entity.event.event_entity import EventEntity
import event_detail as ed
from services.event_service import EventService
from datetime import datetime
from services.general_service import GeneralService
import event_list as ud


event_service = EventService()
general_service = GeneralService()

__root:Toplevel =None
__body_frame:Frame=None
__selectedIndex:int = 0


def run():
    global __root,__body_frame
    __root =Tk()
    app_drawer_frame=side_bar()
    app_drawer_frame.pack(side=LEFT,anchor='ne')
    __body_frame=Frame(__root)
    __body_frame.pack(fill='both',side=RIGHT,expand=1)
    draw_side_bar()
    # 
    __root.mainloop()

def side_bar()->Frame:
    app_drawer_frame = Frame(__root)
    
    Button(app_drawer_frame,text='event list',command=lambda :updateIndex(0)).pack()
    Button(app_drawer_frame,text='create event',command=lambda :updateIndex(1)).pack()
    
    Button(app_drawer_frame,text='Ticket List',command=lambda :updateIndex(2)).pack()
    
    Button(app_drawer_frame,text='User List',command=lambda :updateIndex(3)).pack()
    Button(app_drawer_frame,text='Log out',command=lambda :updateIndex(4)).pack()
    return app_drawer_frame
    

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
        case 4:
            import authentication as auth
            auth.loginPage()    
                                   
        
def updateIndex(i:int):
    global __selectedIndex
    if(__selectedIndex==i):return
    __selectedIndex=i   
    draw_side_bar() 
    
    
if(__name__=="__main__"):
    run()   