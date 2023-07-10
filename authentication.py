
from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk,Image
from assets import *
from services.auth_service import AuthService

authService = AuthService()

def __configureTopWindow()->Tk:
    root=Tk()
    root.geometry("800x500")
    root.iconbitmap(App_Icon)
    root.title("Festivalika")
    root.config(bg="#ffffff")
    return root

def __registerPage():
    registerWindow=__configureTopWindow()
    # configuring reg
    registerWindow.columnconfigure(0,weight=1)
    registerWindow.rowconfigure(0,weight=1)

    # for image
    bckImage=ImageTk.PhotoImage(Image.open(Register_Background).resize((1300,750),Image.LANCZOS))
    Label(registerWindow,image=bckImage).grid(row=0,column=0)

    # for frame
    registerFrame=LabelFrame(registerWindow,bg="#d8d8d8",border=0)
    registerFrame.grid(row=0,column=0,ipady=90)

    # Configure frame
    registerFrame.columnconfigure(0,weight=1)
    registerFrame.rowconfigure((0,1,2,3,4,5,6,7),weight=1)

    # widgets inside frame
    Label(registerFrame,text="Sign up",font=('Arial',"18","bold"),bg='#d8d8d8',fg="#6a3bff").grid(row=0,column=0,sticky='sw',padx=25,ipady=7)
    Label(registerFrame,text="Email",font=('Arial',10,'bold'),bg='#d8d8d8').grid(row=1,column=0,sticky='sw',padx=25)
    emailAddressEntry=Entry(registerFrame,width=50,border=0)
    emailAddressEntry.grid(row=2,column=0,sticky='nw',padx=25,ipady=8)
    Label(registerFrame,text="Password",font=('Arial',10,'bold'),bg='#d8d8d8').grid(row=3,column=0,sticky='sw',padx=25)
    passwordEntry=Entry(registerFrame,width=50,border=0)
    passwordEntry.grid(row=4,column=0,sticky='nw',padx=25,ipady=8)
    Label(registerFrame,text="Confirm Password",font=('Arial',10,'bold'),bg='#d8d8d8').grid(row=5,column=0,sticky='sw',padx=25)
    confirmPasswordEntry=Entry(registerFrame,width=50,border=0)
    confirmPasswordEntry.grid(row=6,column=0,sticky='nw',padx=25,ipady=8)
    registerButton=Button(registerFrame,text="Sign up",font=("arial",10,"bold"),bg="#6a3bff",fg="white")
    registerButton.grid(row=7,column=0,sticky='wen',padx=25,pady=25,ipady=12)
    registerWindow.mainloop()
  
  

  
def loginPage(): 
    loginWindow = __configureTopWindow()
    def onRegisterPressed():
        loginWindow.destroy()
        __registerPage()
           
    # loginFormFrame
    loginFormFrame=LabelFrame(loginWindow,bg="#ffffff",padx=30,border=0)
    loginFormFrame.pack(side="right",expand=True,fill=BOTH,pady=100)
    imageFrame=LabelFrame(loginWindow,border=0)
    imageFrame.pack(side="left",expand=True,fill=BOTH)
    
    # for image
    loginImg=ImageTk.PhotoImage(Image.open(Login_Background).resize((1300,750),Image.LANCZOS))
    Label(imageFrame,image=loginImg).pack(expand=1,fill=BOTH)
    
    # configuring loginFormFrame using grid
    loginFormFrame.columnconfigure((0,1),weight=1)
    loginFormFrame.rowconfigure((0,1,2,3,4,5,6,7),weight=1)

    # title
    Label(loginFormFrame,text="Welcome to",font=('Helvetica',14,'bold'),bg="#ffffff").grid(row=0,column=0,sticky='ws')
    Label(loginFormFrame,text="Festivila",font=('Helvetica',30,"bold"),fg="#6a3bff",bg="#ffffff").grid(row=1,column=0,sticky='wn')

    # Form
    Label(loginFormFrame,text="Email",font=('Arial',10,'bold'),bg="#ffffff").grid(row=2,column=0,sticky='w')
    emailAddress=Entry(loginFormFrame,font=('Arial',20),bg="#eeeeee",border=0)
    emailAddress.grid(row=3,column=0,sticky='n',columnspan=2)
    Label(loginFormFrame,text="Password",font=('Arial',10,'bold'),bg="#ffffff").grid(row=4,column=0,sticky='w')
    password=Entry(loginFormFrame,font=('Arial',20),bg="#eeeeee",border=0)
    password.grid(row=5,column=0,sticky='n',columnspan=2)
    
    # Function to call when press [Login] button
    def onLogin():
        try:
            # emailAddress.get1()
            authService.loginUser(emailAddress.get(),password.get())
        except BaseException as error:
            mb.showerror(message=str(error),title="Error")   
    
    loginButton=Button(loginFormFrame,text="Login",fg="white",bg="#6a3bff",command=onLogin)
    loginButton.grid(row=6,column=0,columnspan=2,sticky="nwe",ipady=8)
    Label(loginFormFrame,text="Don't have an account?",font=('Arial',8,'bold'),bg="#ffffff").grid(row=7,column=0,sticky="ne")
    Button(loginFormFrame,text="Register",bg="#ffffff",font=('Arial',8,'bold'),fg="#6a3bff",border=0,command=onRegisterPressed).grid(row=7,column=1,sticky="nw")
    loginWindow.mainloop()