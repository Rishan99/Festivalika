from tkinter import *
from PIL import ImageTk,Image

fest=Tk()

fest.geometry("800x500")
# title and icon
fest.title("LOGIN")
fest.iconbitmap("D:\\gui\\pic\\event.ico")
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
y=Label(frame,text="Register",bg="#ffffff",font=('Arial',8,'bold'),fg="#6a3bff")
y.grid(row=7,column=1,sticky="nw")

# for images
img=Image.open("pic/con1.jpg")
resize=img.resize((1000,800),Image.ANTIALIAS)
nimg=ImageTk.PhotoImage(resize)
label=Label(frame1,image=nimg)
label.pack(side="left")
fest.mainloop()
