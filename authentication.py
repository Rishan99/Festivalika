
from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk,Image
from utility.assets import *
from entity.user_entity import UserEntity
from services.auth_service import AuthService
from services.general_service import GeneralService
from services.user_provider import UserProvider
from utility.helper import error_message_box
import dashboard as dashboard
authService = AuthService()

genderList:list=GeneralService().getGenderList()

def __configureTopWindow()->Tk:
    root=Tk()
    root.geometry("800x500")
    root.iconbitmap(App_Icon)
    root.title(App_Name)
    root.config(bg=backgroundColor)
    root.resizable(0,0)
    return root

def loginPage(): 
    loginWindow = __configureTopWindow()
    def onRegisterPressed():
        loginWindow.destroy()
        __registerPage()
           
    # loginFormFrame
    loginFormFrame=LabelFrame(loginWindow,bg=backgroundColor,padx=30,border=0)
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
    Label(loginFormFrame,text="Welcome to",font=('Helvetica',14,'bold'),bg=backgroundColor).grid(row=0,column=0,sticky='ws')
    Label(loginFormFrame,text=App_Name,font=('Helvetica',30,"bold"),fg=primaryColor,bg=backgroundColor).grid(row=1,column=0,sticky='wn')

    # Form
    Label(loginFormFrame,text="Email",font=('Arial',10,'bold'),bg=backgroundColor).grid(row=2,column=0,sticky='w')
    emailAddress=Entry(loginFormFrame,font=('Arial',20),bg=inputFieldFillColor,border=0)
    emailAddress.grid(row=3,column=0,sticky='n',columnspan=2)
    Label(loginFormFrame,text="Password",font=('Arial',10,'bold'),bg=backgroundColor).grid(row=4,column=0,sticky='w')
    password=Entry(loginFormFrame,font=('Arial',20),bg=inputFieldFillColor,border=0,show="*")
    password.grid(row=5,column=0,sticky='n',columnspan=2)
    
    # Function to call when press [Login] button
    def onLogin():
        try:
            # emailAddress.get1()
           user= authService.loginUser(emailAddress.get(),password.get())
           UserProvider().initialize_user(user)
           loginWindow.destroy()
           dashboard.run()
        except BaseException as error:
            error_message_box(str(error))
    
    loginButton=Button(loginFormFrame,text="Login",fg="white",bg=primaryColor,command=onLogin)
    loginButton.grid(row=6,column=0,columnspan=2,sticky="nwe",ipady=8)
    Label(loginFormFrame,text="Don't have an account?",font=('Arial',8,'bold'),bg=backgroundColor).grid(row=7,column=0,sticky="ne")
    Button(loginFormFrame,text="Register",bg=backgroundColor,font=('Arial',8,'bold'),fg=primaryColor,border=0,command=onRegisterPressed).grid(row=7,column=1,sticky="nw")
    loginWindow.mainloop()
    
    

def __registerPage():
    registerWindow=__configureTopWindow()

    genderId:int=None
    # configuring reg
    registerWindow.columnconfigure(0,weight=1)
    registerWindow.rowconfigure(0,weight=1)
    # for image
    bckImage=ImageTk.PhotoImage(Image.open(Register_Background).resize((registerWindow.winfo_screenheight(),registerWindow.winfo_screenwidth()),Image.LANCZOS))
    background_label = Label(registerWindow,image=bckImage)
    background_label.grid(row=0,column=0)
    
    

    # for frame
    registerFrame=LabelFrame(registerWindow,bg=backgroundColor,border=0,padx=25)
    registerFrame.grid(row=0,column=0,ipady=90)

    # Configure frame
    registerFrame.columnconfigure(0,weight=1)
    registerFrame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,13),weight=1)
    genderVar=StringVar(value="Select a gender")
    def onGenderSelect(x):
        nonlocal genderId
        gender=next(filter(lambda z:z.name == x,genderList), None)
        if(gender is not None):
            genderId=gender.id

    # widgets inside frame
    Label(registerFrame,text="Sign up",font=('Arial',"18","bold"),bg=backgroundColor,fg=primaryColor).grid(row=0,column=0,sticky='sw',ipady=7)
    row =1
    # 
    Label(registerFrame,text="Name",font=('Arial',10,'bold'),bg=backgroundColor).grid(row=row,column=0,sticky='sw')
    row+=1
    nameEntry=Entry(registerFrame,width=50,border=0,bg=inputFieldFillColor,)
    defineEntryBoxPlace(row,nameEntry)
    row+=1
    # 
    Label(registerFrame,text="Address",font=('Arial',10,'bold'),bg=backgroundColor).grid(row=row,column=0,sticky='sw')
    addressEntry=Entry(registerFrame,width=50,border=0,bg=inputFieldFillColor)
    row+=1
    defineEntryBoxPlace(row,addressEntry)
    row+=1
    #  
    Label(registerFrame,text="Username",font=('Arial',10,'bold'),bg=backgroundColor).grid(row=row,column=0,sticky='sw')
    row+=1
    emailAddressEntry=Entry(registerFrame,width=50,border=0,bg=inputFieldFillColor)
    defineEntryBoxPlace(row,emailAddressEntry)
    row+=1
    #  
    Label(registerFrame,text="Gender",font=('Arial',10,'bold'),bg=backgroundColor,).grid(row=row,column=0,sticky='sw') 
    row+=1
    dropdown_menu = OptionMenu(registerFrame,genderVar, *list(map(lambda x:x.name,GeneralService().getGenderList())),command=lambda x:onGenderSelect(x) ) 
    defineEntryBoxPlace(row,dropdown_menu)
    row+=1
    # 
    Label(registerFrame,text="Password",font=('Arial',10,'bold'),bg=backgroundColor).grid(row=row,column=0,sticky='sw')
    passwordEntry=Entry(registerFrame,width=50,border=0,bg=inputFieldFillColor)
    row+=1
    defineEntryBoxPlace(row,passwordEntry)
    row+=1
    
    # 
    Label(registerFrame,text="Confirm Password",font=('Arial',10,'bold'),bg=backgroundColor).grid(row=row,column=0,sticky='sw')
    confirmPasswordEntry=Entry(registerFrame,width=50,border=0,bg=inputFieldFillColor)
    row+=1
    
    defineEntryBoxPlace(row,confirmPasswordEntry)
    row+=1
    def onRegisterPressed():
        registerWindow.destroy()
        loginPage()
        # Function to call when press [Login] button
    def onRegister():
        try:
            if(genderId is None):
                raise Exception("Gender is required")
            if(passwordEntry.get() != confirmPasswordEntry.get() or len(passwordEntry.get().strip())<1 ):
                raise Exception("Password cannot be empty and should be same as confirm password")
            # emailAddress.get1()
            user= authService.registerUser(UserEntity(nameEntry.get(),emailAddressEntry.get(),addressEntry.get(),genderId,0,passwordEntry.get(),))
            UserProvider().initialize_user(user)
            registerWindow.destroy()
            loginPage()
        #     runUserDashboard()
        except BaseException as error:
            error_message_box(str(error))  
    registerButton=Button(registerFrame,text="Sign up",font=("arial",10,"bold"),bg=primaryColor,fg="white",command=onRegister)
    registerButton.grid(row=row,column=0,sticky='wen',pady=25,ipady=8)
    row+=1
    login_text_frame = Frame(registerFrame,bg=backgroundColor)
    login_text_frame.grid(row=row,column=0,sticky='ne')
    Label(login_text_frame,text="Already have an account?",font=('Arial',8,'bold'),bg=backgroundColor).pack(side=LEFT,)
    Button(login_text_frame,text="Login",bg=backgroundColor,font=('Arial',8,'bold'),fg=primaryColor,border=0,command=onRegisterPressed).pack(side=RIGHT)
    Frame(registerFrame,bg=backgroundColor,pady=20).grid(row=row+1,column=0)
    registerWindow.mainloop()
  
def defineEntryBoxPlace(row:int,widget:Widget):
    widget.grid(row=row,column=0,sticky='nw',ipady=8,)

  