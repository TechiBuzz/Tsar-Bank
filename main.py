# Imports
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
import random
import pickle

# CustomTkinter Settings
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

# THE HOLY GODLY UPHOLDER (the entire program literally runs on this one single dictionary lol)
accounts = {}

# LOAD ACCOUNTS FROM DATA FILE
# feeling paraoud indian bcz i did most of this on my own
while True:
    try:
        accounts = pickle.load(open('data.pkl', 'rb'))
        print('Account data found and imported successfully!')
        break
    except FileNotFoundError:
        print('Account data could not be found, created a new file with default data')
        with open('data.pkl', 'wb') as file:
            pickle.dump({1000000:{'name':'example','password':'examplepassword','age':69,'balance':0}}, file)

# +============================================+ ENTRYPOINT +============================================+ #
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

# +============================================+ MAIN PAGE +============================================+ #
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

# +========================================+ LOGIN ACCOUNT PAGE +========================================+ #
class LoginPage(ctk.CTkFrame):

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
        accountnum_label = ctk.CTkLabel(boxframe, text='Account Number:', font=labelfont)
        accountnum_label.grid(row=0,column=0, padx=10, pady=8)

        password_label = ctk.CTkLabel(boxframe, text='Password:', font=labelfont)
        password_label.grid(row=1,column=0, padx=10, pady=8, sticky='w')

        # ENTRIES
        accountnum_entry = ctk.CTkEntry(boxframe, width=width, height=height, font=entryfont, corner_radius=50)
        accountnum_entry.grid(row=0,column=1, pady=8)

        password_entry = ctk.CTkEntry(boxframe, width=width, height=height, font=entryfont, show='*', corner_radius=50)
        password_entry.grid(row=1,column=1, pady=8)

        boxframe.place(relx=0.5,rely=0.45, anchor=CENTER)

        # FRAME TO HOLD SUBMIT AND CLEAR BUTTONS
        lowerframe = ctk.CTkFrame(self, fg_color='transparent')
        lowerframe.place(relx=0.5, rely=0.7, anchor=CENTER)
        # CREATING SUBMIT AND CLEAR BUTTONS
        ButtonManager.create_bottom_buttons(lowerframe, None, [accountnum_entry, password_entry], 320)

        # BACK BUTTON
        ButtonManager.create_back_button(self, container)
    
# +========================================+ CREATE ACCOUNT PAGE +========================================+ #
class CreatePage(ctk.CTkFrame):
    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)  # Call super

        # COMMONS
        width = 450
        height = 55
        labelfont = ('ADLaM Display', 40, 'bold')
        entryfont = ('Bahnschrift Light', 32, 'bold')
        errorlabel = ctk.CTkLabel(self, text='Error!',font=('Bahnschrift Light', 22))
        # 'Age must be an integer!'
        # 'Invalid Username or Password! Don\'t leave anything empty!'
        # FRAME TO HOLD ALL
        boxframe = ctk.CTkFrame(self, fg_color='transparent')

        # BACK BUTTON
        ButtonManager.create_back_button(self, container)

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

        boxframe.place(relx=0.5,rely=0.4, anchor=CENTER)

        # SUBMIT BUTTON FUNCTIONALITY
        def submit_create():
            # TAKE STUFF
            username = username_entry.get()
            password = password_entry.get()
            age = age_entry.get()

            # VALIDATION
            if username == '' or password == '':
                errorlabel.configure(text='Invalid Username or Password! Don\'t leave anything empty!')
                errorlabel.place(relx=0.5, rely=0.61, anchor=CENTER)
            elif not username.isalpha():
                errorlabel.configure(text='Username cannot contain numbers!')
                errorlabel.place(relx=0.5, rely=0.61, anchor=CENTER)
            elif password.__contains__(' '):
                errorlabel.configure(text='Password cannot contain whitespaces!')
                errorlabel.place(relx=0.5, rely=0.61, anchor=CENTER)
            elif not age.isdigit():
                errorlabel.place_forget() # Remove the previous error
                errorlabel.configure(text='Age must be an integer!')
                errorlabel.place(relx=0.5, rely=0.61, anchor=CENTER)
            else: 
                errorlabel.place_forget() # Remove the error
            
                username_entry.delete(0, len(username)) # Clear username entry box
                password_entry.delete(0, len(password)) # Clear password entry box
                age_entry.delete(0, len(age)) # Clear age entry box
                AccountManager.create_new_account(username=username, password=password, age=age)
                container.show_frame(MainPage)

        # # CLEAR BUTTON FUNCTIONALITY
        # def clear_entries():
        #     errorlabel.place_forget() # Remove the error label
        #     username_entry.delete(0, len(username_entry.get())) # Clear username entry box
        #     password_entry.delete(0, len(password_entry.get())) # Clear password entry box
        #     age_entry.delete(0, len(age_entry.get())) # Clear age entry box

        # FRAME TO HOLD SUBMIT AND CLEAR BUTTONS
        lowerframe = ctk.CTkFrame(self, fg_color='transparent')
        lowerframe.place(relx=0.5, rely=0.7, anchor=CENTER)
        # CREATING SUBMIT AND CLEAR BUTTONS
        ButtonManager.create_bottom_buttons(lowerframe, submit_create, [username_entry, password_entry, age_entry], 320)     

        # INFORMATICS
        info_icon = ctk.CTkImage(dark_image=Image.open('info.png'))
        info = ctk.CTkLabel(self, 
                            text='  Please ensure the details are correct as once submitted they cannot be changed!',
                            font=('Bahnschrift Light', 16),
                            image=info_icon, compound=LEFT)
        info.place(relx=0.5, rely=0.9, anchor=CENTER)

# +==========================================+ ACCOUNT MANAGER +==========================================+ #
class AccountManager:

    # Method to create new account (its self explanatory)
    def create_new_account(username, password, age):
        # Create random account number
        accountnumber = random.randint(1000000, 9999999)
        while accountnumber in accounts.keys(): # Make sure account number is unique
            accountnumber = random.randint(1000000, 9999999)

        # Update dictionaty and file
        accounts.update({accountnumber : {'name':username,'password':password,'age':age,'balance':0}})
        with open('data.pkl', 'wb') as file:
            pickle.dump(accounts, file)

    def log_into_account(accountnumer, password) -> dict:
        return {}

# +==========================================+ COMMON BUTTONS +==========================================+ #

class ButtonManager:

    def create_bottom_buttons(container, submitcmd, clearentries, width=320):

        # Clear button functionality
        def clear_entries(entries=clearentries):
            for entry in entries: entry.delete(0, len(entry.get()))

        submit = ctk.CTkButton(container,
               text='Submit',
               font=('ADLaM Display', 22, 'bold'),
               width=width,
               height=50,
               corner_radius=30,
               command=submitcmd)
        clear = ctk.CTkButton(container,
               text='Clear',
               font=('ADLaM Display', 22, 'bold'),
               width=width,
               height=50,
               corner_radius=30,
               command=clear_entries)
        submit.pack(side=LEFT, padx=10)
        clear.pack(side=RIGHT, padx=10)

    def create_back_button(container, main):
        back = ctk.CTkButton(container,
               text='Back',
               font=('ADLaM Display', 22, 'bold'),
               width=80,
               height=50,
               corner_radius=30,
               command=lambda: main.show_frame(MainPage))
        back.place(relx=0.1, rely=0.1, anchor=CENTER)

# +============================================+ ENTRYPOINT +============================================+ #

if __name__ == "__main__":
    app = MainApp()
    app.geometry('1024x576')
    app.resizable(False, False)
    app.mainloop()