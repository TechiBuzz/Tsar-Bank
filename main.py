# Imports
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
import random
import pickle

# CustomTkinter Settings
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

# GLOBAL VARS
accounts = {}
# LOAD ACCOUNTS FROM DATA FILE
while True:
    try:
        accounts = pickle.load(open('data.pkl', 'rb'))
        print('Account data found and imported successfully!')
        break
    except FileNotFoundError:
        print('Account data could not be found, created a new file with default data')
        with open('data.pkl', 'wb') as file:
            pickle.dump({1000:{'name':'example','password':'examplepassword','age':69}}, file)

class MainApp(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self) # Call super

        self.title('Tsar Bank')
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)  # Use the appropriate geometry manager

        self.frames = {}
        for Page in (MainPage, LoginPage, CreatePage):
            frame = Page(self.container, self)
            self.frames[Page] = frame
            frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(MainPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent) # Call super

        # WELCOME LABEL
        welcome = ctk.CTkLabel(self,
                text='Welcome to Tsar Bank!',
                font=('ADLaM Display', 60, 'bold'))
        welcome.place(relx=0.5, rely= 0.2, anchor=CENTER)

        # COMMONS
        width=500
        height=60

        # LOGIN BUTTON
        login = ctk.CTkButton(self,
               text='Log in to an existing account',
               font=('ADLaM Display', 23, 'bold'),
               width=width,
               height=height,
               corner_radius=30,
               command=lambda: container.show_frame(LoginPage))
        login.place(relx=0.5, rely=0.48, anchor=CENTER)
        
        # CREATE BUTTON
        create = ctk.CTkButton(self,
               text='Create a new account',
               font=('ADLaM Display', 23, 'bold'),
               width=width,
               height=height,
               corner_radius=30,
               command=lambda: container.show_frame(CreatePage))
        create.place(relx=0.5, rely=0.6, anchor=CENTER)

class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)  # Call super

        # COMMONS
        width = 450
        height = 55
        labelfont = ('ADLaM Display', 40, 'bold')
        entryfont = ('Bahnschrift Light', 32, 'bold')
        errorlabel = ctk.CTkLabel(self, text='Username or Password is invalid!',font=('Bahnschrift Light', 22))

        # FRAME TO HOLD ALL
        boxframe = ctk.CTkFrame(self, fg_color='transparent', corner_radius=40)

        # LABELS
        username_label = ctk.CTkLabel(boxframe, text='Username:', font=labelfont)
        username_label.grid(row=0,column=0, padx=10, pady=8)

        password_label = ctk.CTkLabel(boxframe, text='Password:', font=labelfont)
        password_label.grid(row=1,column=0, padx=10, pady=8)

        # ENTRIES
        username_entry = ctk.CTkEntry(boxframe, width=width, height=height, font=entryfont, corner_radius=50)
        username_entry.grid(row=0,column=1, pady=8)

        password_entry = ctk.CTkEntry(boxframe, width=width, height=height, font=entryfont, show='*', corner_radius=50)
        password_entry.grid(row=1,column=1, pady=8)

        boxframe.place(relx=0.5,rely=0.45, anchor=CENTER)

        # BACK BUTTON
        back = ctk.CTkButton(self,
               text='Back',
               font=('ADLaM Display', 22, 'bold'),
               width=80,
               height=50,
               corner_radius=30,
               command=lambda: container.show_frame(MainPage))
        back.place(relx=0.1, rely=0.1, anchor=CENTER)
    
        # SUBMIT BUTTON FUNCTIONALITY
        def submit_login():
            username = username_entry.get()
            password = password_entry.get()
            
            if username == '' or password == '':
                errorlabel.place(relx=0.5, rely=0.6, anchor=CENTER)
            else: 
                errorlabel.place_forget() # Remove the error
                username_entry.delete(0, len(username)) # Clear username entry box
                password_entry.delete(0, len(password)) # Clear password entry box
                AccountManager.create_new_account(username=username, password=password, age=1)
                print(accounts)

        # SUBMIT BUTTON
        submit = ctk.CTkButton(self,
               text='Submit',
               font=('ADLaM Display', 22, 'bold'),
               width=500,
               height=50,
               corner_radius=30,
               command=submit_login)
        submit.place(relx=0.5, rely=0.7, anchor=CENTER)

class CreatePage(ctk.CTkFrame):
    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)  # Call super

        # COMMONS
        width = 450
        height = 55
        labelfont = ('ADLaM Display', 40, 'bold')
        entryfont = ('Bahnschrift Light', 32, 'bold')

        # FRAME TO HOLD ALL
        boxframe = ctk.CTkFrame(self, fg_color='transparent', corner_radius=40)

        # LABELS
        username_label = ctk.CTkLabel(boxframe, text='Username:', font=labelfont)
        username_label.grid(row=0,column=0, padx=10, pady=8)

        password_label = ctk.CTkLabel(boxframe, text='Password:', font=labelfont)
        password_label.grid(row=1,column=0, padx=10, pady=8, sticky='w')
        
        age_label = ctk.CTkLabel(boxframe, text='Age:', font=labelfont)
        age_label.grid(row=2,column=0, padx=10, pady=8, sticky='w')

        # ENTRIES
        username_entry = ctk.CTkEntry(boxframe, width=width, height=height, font=entryfont, corner_radius=50)
        username_entry.grid(row=0,column=1, pady=8)

        password_entry = ctk.CTkEntry(boxframe, width=width, height=height, font=entryfont, show='*', corner_radius=50)
        password_entry.grid(row=1,column=1, pady=8)
        
        age_entry = ctk.CTkEntry(boxframe, width=width, height=height, font=entryfont, corner_radius=50)
        age_entry.grid(row=2,column=1, pady=8)

        boxframe.place(relx=0.5,rely=0.5, anchor=CENTER)

        # BACK BUTTON
        back = ctk.CTkButton(self,
               text='Back',
               font=('ADLaM Display', 22, 'bold'),
               width=80,
               height=50,
               corner_radius=30,
               command=lambda: container.show_frame(MainPage))
        back.place(relx=0.1, rely=0.1, anchor=CENTER)

        # INFORMATICS
        info_icon = ctk.CTkImage(dark_image=Image.open('info.png'))
        info = ctk.CTkLabel(self, 
                            text='  Please ensure the details are correct as once submitted they cannot be changed!',
                            font=('Bahnschrift Light', 16),
                            image=info_icon, compound=LEFT)
        info.place(relx=0.5, rely=0.9, anchor=CENTER)

class AccountManager():
    def create_new_account(username, password, age: int):

        accountnumber = random.randint(1000, 9999)
        while accountnumber in accounts.keys():
            accountnumber = random.randint(1000, 9999)
        print(accountnumber)

        accounts.update({accountnumber : {'name':username,'password':password,'age':age}})

        with open('data.pkl', 'wb') as file:
            pickle.dump(accounts, file)

if __name__ == "__main__":
    app = MainApp()
    app.geometry('1024x576')
    app.resizable(False, False)
    app.mainloop()