from datetime import datetime
from tkinter import messagebox as mb


def convert_datetime_from_database(value:str)->datetime:
    return datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
    
def convert_datetime_to_default(value:datetime)->str:
    return value.strftime("%m/%d/%y")

1
def error_message_box(message:str):
    mb.showerror(title="Error",message=message)
    
    
def success_message_box(message:str):
    mb.showinfo(title="Success",message=message)

        