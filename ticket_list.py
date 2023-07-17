
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from entity.ticket_payment_entity import TicketPaymentEntity
from services.ticket_payment_service import TicketPaymentService
from services.user_provider import UserProvider
from utility.helper import error_message_box
from widgets.scrollable import  ScrollbarFrame

ticket_payment_service = TicketPaymentService()

__root:Toplevel =None
__ticket_payment_list_frame:Frame=None


def run(tk:Widget):
    global __root,dropdown_options,categoryVar,__ticket_payment_list_frame
    __root =tk
    __ticket_payment_list_frame=Frame(__root,)
    __show_ticket_list()
    __ticket_payment_list_frame.pack(expand=1,fill='both')
    __root.mainloop()
  

def __refresh_ticket_list():
    global __ticket_payment_list_frame
    childs = __ticket_payment_list_frame.children.copy()
    for child in childs.values():
        child.destroy()
    __show_ticket_list()

def __show_ticket_list():
    ticket_list= ticket_payment_service.getAllTicketList() if UserProvider().user.isAdmin  else ticket_payment_service.getUserTicketList(UserProvider().user.id)
    if(len(ticket_list)==0):
        Label(__ticket_payment_list_frame,text="No Tickets Payment Found",font=font.Font(weight="normal",size=14,)).pack(fill=BOTH,expand=1,padx=20,pady=20)
    else:    
        __scrollable_body = ScrollbarFrame(__ticket_payment_list_frame,)
        __scrollable_body.pack(fill='both',expand=1, anchor='e')
        ticket_list_frame=__scrollable_body.scrolled_frame
        for ticket_payment in ticket_list:
            ticket_payment_frame = Frame(ticket_list_frame)
            widget=__ticket_widget(ticket_payment_frame,ticket_payment)
            widget.pack(anchor="w",padx=10)
            separator = Separator(ticket_payment_frame, orient='horizontal')
            separator.pack(fill='x',expand=1,pady=5,padx=10,)
            ticket_payment_frame.pack(fill='x',expand=1,anchor='w')
    
      
def __ticket_widget(master,ticket_payment: TicketPaymentEntity)->Widget:
    ticket_payment_frame = Frame(master=master)
    title_label=Label(ticket_payment_frame,text=ticket_payment.eventTitle,font=('Arial',14),anchor="w")
    ticket_status_label=Label(ticket_payment_frame,text=ticket_payment.ticketStatus,font=('Arial',10,))
    user_name_label=Label(ticket_payment_frame,text=ticket_payment.userName,font=('Arial',10,))
    title_label.grid(row=0,column=0,sticky="w")
    ticket_status_label.grid(row=1,column=0,sticky="w")
    user_name_label.grid(row=2,column=0,sticky="w")
    approve_button=Button(ticket_payment_frame,text="Approve",command=lambda i=ticket_payment.id:approve_ticket(i))
    reject_button=Button(ticket_payment_frame,text="Reject",command=lambda i=ticket_payment.id:reject_ticket(i))
    delete_button=Button(ticket_payment_frame,text="Delete",command=lambda i=ticket_payment.id:delete_ticket(i))
    if(UserProvider().user.isAdmin):
        if(ticket_payment.ticketStatusId == 1):
            approve_button.grid(row=3,column=0)
            reject_button.grid(row=3,column=1)
            delete_button.grid(row=3,column=2)
        elif(ticket_payment.ticketStatusId==3):
            delete_button.grid(row=3,column=0)
    return ticket_payment_frame

def approve_ticket(ticket_id:int):
    callback = mb.askyesno(title="Confirm",message="Are you sure you want to approve this payment")
    if(callback):
        try:
            ticket_payment_service.approveEventTicket(ticket_id)
            __refresh_ticket_list()
        except BaseException as ex:
            error_message_box(title="Error",message=str(ex)) 

def delete_ticket(ticket_id:int):
    callback = mb.askyesno(title="Confirm",message="Are you sure you want to delete this payment")
    if(callback):
        try:
            ticket_payment_service.deleteEventTicket(ticket_id)
            __refresh_ticket_list()
        except BaseException as ex:
            error_message_box(title="Error",message=str(ex)) 
            
            
def reject_ticket(ticket_id:int):
    callback = mb.askyesno(title="Confirm",message="Are you sure you want to reject this payment")
    if(callback):
        try:
            ticket_payment_service.rejectEventTicket(ticket_id)
            __refresh_ticket_list()
        except BaseException as ex:
            error_message_box(title="Error",message=str(ex))    
    