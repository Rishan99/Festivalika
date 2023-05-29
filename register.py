from tkinter import *
from PIL import ImageTk,Image
from Imageicon import *
def show_reg():
    global nimg1, frame_reg
    reg=Tk()
    reg.geometry("800x500")

    # title and icon
    reg.title("REGISTER")
    reg.iconbitmap(Img_icon)
    reg.config(bg="#ffffff")

    # configuring reg
    reg.columnconfigure(0,weight=1)
    reg.rowconfigure(0,weight=1)

    # for image
    img1=Image.open(Reg_img)
    resize1=img1.resize((1300,750),Image.LANCZOS)
    nimg1=ImageTk.PhotoImage(resize1)
    label_img=Label(reg,image=nimg1)
    label_img.grid(row=0,column=0)

    # for frame
    frame_reg=LabelFrame(reg,bg="#d8d8d8",border=0)
    frame_reg.grid(row=0,column=0,ipady=90)

    # Configure frame
    frame_reg.columnconfigure(0,weight=1)
    frame_reg.rowconfigure((0,1,2,3,4,5,6,7),weight=1)

    # widgets inside frame
    a=Label(frame_reg,text="Sign up",font=('Arial',"18","bold"),bg='#d8d8d8',fg="#6a3bff")
    a.grid(row=0,column=0,sticky='sw',padx=25,ipady=7)
    e=Label(frame_reg,text="Email",font=('Arial',10,'bold'),bg='#d8d8d8')
    e.grid(row=1,column=0,sticky='sw',padx=25)
    email=Entry(frame_reg,width=50,border=0)
    email.grid(row=2,column=0,sticky='nw',padx=25,ipady=8)
    pword=Label(frame_reg,text="Password",font=('Arial',10,'bold'),bg='#d8d8d8')
    pword.grid(row=3,column=0,sticky='sw',padx=25)
    p_entry=Entry(frame_reg,width=50,border=0)
    p_entry.grid(row=4,column=0,sticky='nw',padx=25,ipady=8)
    cpword=Label(frame_reg,text="Confirm Password",font=('Arial',10,'bold'),bg='#d8d8d8')
    cpword.grid(row=5,column=0,sticky='sw',padx=25)
    cpword_entry=Entry(frame_reg,width=50,border=0)
    cpword_entry.grid(row=6,column=0,sticky='nw',padx=25,ipady=8)
    subu=Button(frame_reg,text="Sign up",font=("arial",10,"bold"),bg="#6a3bff",fg="white")
    subu.grid(row=7,column=0,sticky='wen',padx=25,pady=25,ipady=12)
    # return nimg, frame

    reg.mainloop()

