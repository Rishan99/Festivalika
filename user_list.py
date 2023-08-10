
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from entity.user_entity import UserEntity
from services.auth_service import AuthService
from services.general_service import GeneralService
from services.user_provider import UserProvider
from utility.helper import error_message_box
from widgets.scrollable import  ScrollbarFrame
from utility.assets import *

user_service = GeneralService()

auth_service = AuthService()

__root:Toplevel =None
__user_list_frame:Frame=None


def run(tk:Widget):
    global __root,dropdown_options,categoryVar,__user_list_frame
    __root =tk
    __user_list_frame=Frame(__root,bg=backgroundColor)
    __show_user_list()
    __user_list_frame.pack(expand=1,fill='both')
    # __root.mainloop()
  

def __refresh_user_list():
    global __root
    childs = __root.children.copy()
    for child in childs.values():
        child.destroy()
    __show_user_list()

def __show_user_list():
    
    user_list= user_service.getUserList()
    Label(__user_list_frame,text="User List",font=font.Font(weight="bold",size=16),bg=backgroundColor).pack(padx=10,anchor='w',pady=(10,0))  
    Label(__user_list_frame,text=f'Total Users: {len(user_list)}',bg=backgroundColor).pack(padx=10,anchor='w',pady=(0,5))
    if(len(user_list)==0):
        Label(__user_list_frame,text="No User Found",font=font.Font(weight="normal",size=14,)).pack(fill=BOTH,expand=1,padx=80,pady=20)
    else:    
        __scrollable_body = ScrollbarFrame(__user_list_frame,)
        __scrollable_body.pack(fill='both',expand=1, anchor='e')
        user_list_frame=__scrollable_body.scrolled_frame
        user_list_frame.config(bg=backgroundColor)
        for user in user_list:
            user_frame = Frame(user_list_frame,bg='#999999')
            widget=__user_widget(user_frame,user)
            widget.pack(anchor="w",fill=X)
            user_frame.pack(fill='x',expand=1,anchor='w')
            Frame(user_list_frame,height=10,width=9999).pack(expand=1,fill=Y)
    
#    change heree   
def __user_widget(master,user: UserEntity)->Widget:
    user_frame = Frame(master=master,bg=backgroundColor,padx=10,pady=10)
    name_label=Label(user_frame,text=user.name,font=('Arial',14),anchor="w",bg=backgroundColor)
    username_label=Label(user_frame,text=user.username,font=('Arial',10,),bg=backgroundColor)
    name_label.grid(row=0,column=0,sticky="w")
    username_label.grid(row=1,column=0,sticky="w")
    
    delete_button=Button(user_frame,text="Delete",command=lambda i=user.id:delete_user(i))
    if(UserProvider().user.isAdmin):
            delete_button.grid(row=3,column=0,sticky='w')
    return user_frame


def delete_user(ticket_id:int):
    callback = mb.askyesno(title="Confirm",message="Are you sure you want to delete this user, All the tickets of this user will also be delete")
    if(callback):
        try:
            auth_service.deleteUser(ticket_id)
            __refresh_user_list()
        except BaseException as ex:
            error_message_box(message=str(ex)) 

    