
from tkinter import *
from PIL import ImageTk,Image
from Imageicon import *


fest=Tk()
fest.geometry("800x500")

def show_reg():
    fest.destroy()
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
    frame_reg.pack(row=0,column=0,ipady=90)

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
   
    
    reg.mainloop()
  

# title and icon
fest.title("LOGIN")
fest.iconbitmap(Img_icon)
fest.config(bg="#ffffff")

# frame
frame=LabelFrame(fest,bg="#ffffff",padx=30,border=0)
frame.pack(side="right",expand=True,fill=BOTH,pady=100)
frame1=LabelFrame(fest,border=0)
frame1.pack(side="right",expand=True,fill=BOTH)

# configuring frame1 using grid
frame.columnconfigure(0,weight=1)
frame.columnconfigure(1,weight=1)
frame.rowconfigure(0,weight=1)
frame.rowconfigure(1,weight=1)
frame.rowconfigure(2,weight=1)
frame.rowconfigure(3,weight=1)
frame.rowconfigure(4,weight=1)
frame.rowconfigure(5,weight=1)
frame.rowconfigure(6,weight=1)
frame.rowconfigure(7,weight=1)

# introduction
a=Label(frame,text="Welcome to",font=('Helvetica',14,'bold'),bg="#ffffff")
a.grid(row=0,column=0,sticky='ws')
b=Label(frame,text="Festivila",font=('Helvetica',30,"bold"),fg="#6a3bff",bg="#ffffff")
b.grid(row=1,column=0,sticky='wn')

# login and password label and entry
email=Label(frame,text="Email",font=('Arial',10,'bold'),bg="#ffffff")
email.grid(row=2,column=0,sticky='w')
e=Entry(frame,font=('Arial',20),bg="#eeeeee",border=0)
e.grid(row=3,column=0,sticky='n',columnspan=2)
pwd=Label(frame,text="Password",font=('Arial',10,'bold'),bg="#ffffff")
pwd.grid(row=4,column=0,sticky='w')
p=Entry(frame,font=('Arial',20),bg="#eeeeee",border=0)
p.grid(row=5,column=0,sticky='n',columnspan=2)
logb=Button(frame,text="Login",fg="white",bg="#6a3bff")
logb.grid(row=6,column=0,columnspan=2,sticky="nwe",ipady=8)
x=Label(frame,text="Don't have an account?",font=('Arial',8,'bold'),bg="#ffffff")
x.grid(row=7,column=0,sticky="ne")
y=Button(frame,text="Register",bg="#ffffff",font=('Arial',8,'bold'),fg="#6a3bff",border=0,command=show_reg)
y.grid(row=7,column=1,sticky="nw")

# for image
img=Image.open(Fram1_img)
resize=img.resize((1000,800),Image.LANCZOS)
nimg=ImageTk.PhotoImage(resize)
label=Label(frame1,image=nimg)
label.pack(side="left")

fest.mainloop()
