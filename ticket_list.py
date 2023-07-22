
from functools import reduce
from tkinter import *
from tkinter import font
from tkinter import messagebox as mb
from tkinter.ttk import Separator
from entity.ticket_count_entity import TickeCountEntity
from entity.ticket_payment_entity import TicketPaymentEntity
from services.ticket_payment_service import TicketPaymentService
from services.user_provider import UserProvider
from utility.helper import error_message_box
from widgets.scrollable import  ScrollbarFrame
from utility.assets import *

ticket_payment_service = TicketPaymentService()

__root:Widget =None
__ticket_payment_list_frame:Frame=None


def run(tk:Widget):
    global __root,dropdown_options,categoryVar,__ticket_payment_list_frame
    __root =tk
    __ticket_payment_list_frame=Frame(__root,bg=backgroundColor)
    __show_ticket_list()
    __ticket_payment_list_frame.pack(expand=1,fill='both')
    # __root.mainloop()
  

def __refresh_ticket_list():
    global __ticket_payment_list_frame
    childs = __ticket_payment_list_frame.children.copy()
    for child in childs.values():
        child.destroy()
    __show_ticket_list()
    
    
def countTotalTicketByStatus(initial:TickeCountEntity,data:TicketPaymentEntity)->TickeCountEntity:
    match data.ticketStatusId:
        case 1:
            initial.pendingCount+=1
        case 2:
            initial.approvedCount+=1
        case 3:
            initial.RejectedCount+=1
    return initial
        

def __show_ticket_list():
    ticket_list= ticket_payment_service.getAllTicketList() if UserProvider().user.isAdmin  else ticket_payment_service.getUserTicketList(UserProvider().user.id)
    count_data=reduce(countTotalTicketByStatus,ticket_list,TickeCountEntity(0,0,0))
    Label(__ticket_payment_list_frame,text=f"{'Take a look at all your tickets' if not UserProvider().user.isAdmin else 'Here are list of all the tickets'} ({len(ticket_list)})",font=font.Font(size=13,weight="bold"),bg=backgroundColor).pack(padx=10,anchor='w')
    Label(__ticket_payment_list_frame,text=f"Approved: {count_data.approvedCount}, Pending: {count_data.pendingCount}, Rejected : {count_data.RejectedCount}",bg=backgroundColor,).pack(padx=10,anchor='w')
    if(len(ticket_list)==0):
        Label(__ticket_payment_list_frame,text="No Tickets Payment Found",font=font.Font(weight="normal",size=14,),bg=backgroundColor).pack(fill=BOTH,expand=1,padx=20,pady=20)
    else:    
        __scrollable_body = ScrollbarFrame(__ticket_payment_list_frame,)
        __scrollable_body.pack(fill='both',expand=1, anchor='e',pady=20)
        ticket_list_frame=__scrollable_body.scrolled_frame
        for ticket_payment in ticket_list:
            ticket_payment_frame = Frame(ticket_list_frame,bg=backgroundColor,width=300)
            widget=__ticket_widget(ticket_payment_frame,ticket_payment)
            widget.pack(anchor="w",padx=10,fill=X)
            ticket_payment_frame.pack(fill='x',expand=1,anchor='w',pady=2)
    
      
def __ticket_widget(master,ticket_payment: TicketPaymentEntity)->Widget:
    statusColor= pendingColor  if ticket_payment.ticketStatusId==2 else approvedColor if ticket_payment.ticketStatusId==1 else rejectedColor
    ticket_payment_frame = Frame(master=master,pady=15,bg=backgroundTileColor,padx=15)
    Label(ticket_payment_frame,text=ticket_payment.eventTitle,font=('Arial',12),anchor="w",bg=backgroundTileColor).grid(row=0,column=0,sticky="w")
    Label(ticket_payment_frame,text=f'Venue: {ticket_payment.address}',anchor="w",bg=backgroundTileColor).grid(row=1,column=0,sticky="w")
    Label(ticket_payment_frame,text=f'Bought By: {ticket_payment.userName}',bg=backgroundTileColor).grid(row=2,column=0,sticky="w")
    Label(ticket_payment_frame,text=f'Status: {ticket_payment.ticketStatus}',fg=statusColor,bg=backgroundTileColor).grid(row=3,column=0,sticky="w")
    Label(ticket_payment_frame,text=f'Price: {ticket_payment.price}',bg=backgroundTileColor,).grid(row=4,column=0,sticky="w")
    button_frame = Frame(ticket_payment_frame,bg=backgroundTileColor)
    button_frame.grid(row=5,column=0)
    approve_button=Button(button_frame,text="Approve",bg='green',fg=backgroundColor,command=lambda i=ticket_payment.id:approve_ticket(i))
    reject_button=Button(button_frame,text="Reject",bg='red',fg=backgroundColor,command=lambda i=ticket_payment.id:reject_ticket(i),)
    delete_button=Button(button_frame,text="Delete",bg='orange',fg=backgroundColor,command=lambda i=ticket_payment.id:delete_ticket(i),)

    if(UserProvider().user.isAdmin):
        if(ticket_payment.ticketStatusId == 1):
            approve_button.pack(side=LEFT,padx=8)
            reject_button.pack(side=LEFT,padx=8)
            delete_button.pack(side=LEFT,padx=8)
        elif(ticket_payment.ticketStatusId==3):
            delete_button.pack(side=LEFT)
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
 