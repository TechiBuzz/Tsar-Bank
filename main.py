
#^ +=============================================+ IMPORTS +=============================================+ #

from tkinter import *
import customtkinter as ctk
from PIL import Image
import random
import pickle

#^ +=========================================+ CUSTOM TKINTER +==========================================+ #

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

#^ +===========================================+ GOD SECTION +===========================================+ #

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
            pickle.dump({1000000:{'name':'example','password':'examplepassword','age':69,'balance':69420}}, file)

#^ +============================================+ ENTRYPOINT +============================================+ #
class MainApp(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self) # Call super

        self.title('Tsar Bank')
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for Page in (MainPage, LoginPage, CreatePage, LoggedInPage):
            frame = Page(self.container, self)
            self.frames[Page] = frame # personal note - for each class assign a value of its instance
            frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(MainPage)

    def show_frame(self, container, *args, **kwargs):
        frame = self.frames[container]
        frame.tkraise()

        if args or kwargs:
            frame.update_accnum(*args)

#^ +============================================+ MAIN PAGE +============================================+ #
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

#^ +========================================+ LOGIN ACCOUNT PAGE +========================================+ #
class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)  # Call super

        # COMMONS
        width = 450
        height = 55
        labelfont = ('ADLaM Display', 40, 'bold')
        entryfont = ('Bahnschrift Light', 32, 'bold')
        infolabel = ctk.CTkLabel(self, text='Error!',font=('Bahnschrift Light', 22))

        # FRAME TO HOLD ALL
        boxframe = ctk.CTkFrame(self, fg_color='transparent', corner_radius=40)

        # BACK BUTTON
        ButtonManager.create_back_button(self, container, infolabel)

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

        # SUMBISSION
        def submit_login():
            
            # Make sure to get account number as integer
            valid_accnum = False
            try:
                accnum = int(accountnum_entry.get())
                valid_accnum = True
            except ValueError:
                infolabel.configure(text='⚠️ Account number can only consist on numbers!')
                infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
            # Get password
            password = password_entry.get()

            # VALIDATION
            if valid_accnum:
                if password.isspace() or password == '':
                    infolabel.configure(text='⚠️ Account number or password field cannot be empty!')
                    infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
                elif not AccountManager.accountnumber_exists(accnum):
                    infolabel.configure(text='⚠️ Account number not found!')
                    infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
                elif not AccountManager.password_matches(accnum, password):
                    infolabel.configure(text='⚠️ Please enter the correct password!')
                    infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
                else:
                    AccountManager.log_into_account(accnum, password, container)
                    accountnum_entry.delete(0, len(str(accnum)))
                    password_entry.delete(0, len(password))

        # CREATING SUBMIT AND CLEAR BUTTONS
        ButtonManager.create_bottom_buttons(self, submit_login, [accountnum_entry, password_entry], 320, 0.8, infolabel)

#^ +========================================+ CREATE ACCOUNT PAGE +========================================+ #
class CreatePage(ctk.CTkFrame):

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)  # Call super

        # COMMONS
        width = 450
        height = 55
        labelfont = ('ADLaM Display', 40, 'bold')
        entryfont = ('Bahnschrift Light', 32, 'bold')
        infolabel = ctk.CTkLabel(self, text='Error!',font=('Bahnschrift Light', 22))

        # FRAME TO HOLD ALL
        boxframe = ctk.CTkFrame(self, fg_color='transparent')

        # BACK BUTTON
        ButtonManager.create_back_button(self, container, infolabel)

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

            def is_valid_username(username):
                for char in username:
                    if not (char.isalpha() or char.isspace()):
                        return False
                return True

            # VALIDATION
            if username == '' or password == '' or username.isspace():
                infolabel.configure(text='⚠️ Invalid Username or Password! Don\'t leave anything empty!')
                infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
            elif not is_valid_username(username):
                infolabel.configure(text='⚠️ Username cannot contain numbers!')
                infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
            elif password.__contains__(' '):
                infolabel.configure(text='⚠️ Password cannot contain whitespaces!')
                infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
            elif not age.isdigit():
                infolabel.configure(text='⚠️ Age must be an integer!')
                infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
            elif not int(age) >= 18:
                infolabel.configure(text='⚠️ Minimum age to sign-up is 18 years!')
                infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)
            else:
                infolabel.place_forget() # Remove the error
            
                username_entry.delete(0, len(username)) # Clear username entry box
                password_entry.delete(0, len(password)) # Clear password entry box
                age_entry.delete(0, len(age)) # Clear age entry box

                # Create account and retrieve the account number
                accnum = AccountManager.create_new_account(username=username.strip(), password=password, age=age)

                infotext = 'You account has been successfully created! \n Your account number is: ' + str(accnum)
            
                infolabel.configure(text=infotext)
                infolabel.place(relx=0.5, rely=0.66, anchor=CENTER)

        # CREATING SUBMIT AND CLEAR BUTTONS
        ButtonManager.create_bottom_buttons(self, submit_create, [username_entry, password_entry, age_entry], 320, 0.8, infolabel)     

        # INFORMATICS
        info_icon = ctk.CTkImage(dark_image=Image.open('info.png'))
        info = ctk.CTkLabel(self, 
                            text='  Please ensure the details are correct as once submitted they cannot be changed!',
                            font=('Bahnschrift Light', 16),
                            image=info_icon, compound=LEFT)
        info.place(relx=0.5, rely=0.9, anchor=CENTER)

#^ +==========================================+ LOGGED IN PAGE +===========================================+ #
class LoggedInPage(ctk.CTkFrame):

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)
        self.current_account = None  # No account selected as of instantiation

        # COMMONS
        width = 600
        height = 60
        buttonfont = ('ADLaM Display', 27, 'bold')

        # BACK BUTTOn
        ButtonManager.create_back_button(self, container, None)

        # BALANCE LABEL
        self.balance_label = ctk.CTkLabel(self,
                                          text='Current Balance: \n$ ',
                                          font=('ADLaM Display', 60, 'bold'))
        self.balance_label.place(relx=0.5, rely=0.18, anchor=CENTER)

        # CREDIT BUTTON
        credit = ctk.CTkButton(self,
                               text='Credit Money To Account',
                               font=buttonfont,
                               width=width,
                               height=height,
                               corner_radius=30,
                               command=lambda: container.show_frame(LoginPage))
        credit.place(relx=0.5, rely=0.45, anchor=CENTER)

        # DEBIT BUTTON
        debit = ctk.CTkButton(self,
                              text='Withdraw Money From Account',
                              font=buttonfont,
                              width=width,
                              height=height,
                              corner_radius=30,
                              command=lambda: container.show_frame(LoginPage))
        debit.place(relx=0.5, rely=0.6, anchor=CENTER)

        # TRANSFER BUTTON
        transfer = ctk.CTkButton(self,
                                 text='Transfer Money To Another Account',
                                 font=buttonfont,
                                 width=width,
                                 height=height,
                                 corner_radius=30,
                                 command=lambda: container.show_frame(LoginPage))
        transfer.place(relx=0.5, rely=0.75, anchor=CENTER)

    def update_accnum(self, accnum):
        self.current_account = accounts[accnum]
        self.update_balance_label(self.current_account['balance'])  # Call the method to update balance label

    def update_balance_label(self, new_balance):
        if self.current_account and 'balance' in self.current_account:
            balance_text = 'Current Balance: \n$ ' + str(new_balance)
            self.balance_label.configure(text=balance_text)

#^ +==========================================+ ACCOUNT MANAGER +==========================================+ #
class AccountManager:

    # Method to create new account (its self explanatory)
    def create_new_account(username, password, age) -> int:
        # Create random account number
        accountnumber = random.randint(1000000, 9999999)
        while accountnumber in accounts.keys(): # Make sure account number is unique
            accountnumber = random.randint(1000000, 9999999)

        # Update dictionaty and file
        accounts.update({accountnumber : {'name':username,'password':password,'age':age,'balance':0}})
        with open('data.pkl', 'wb') as file:
            pickle.dump(accounts, file)

        return accountnumber
    
    def log_into_account(accnum, password, container):
        container.show_frame(LoggedInPage, accnum)
        
    # Helper methods
    def accountnumber_exists(accnum :int):
        return True if accnum in accounts.keys() else False
        
    def password_matches(accnum, password):
        return True if accounts[accnum]['password'] == password else False

#^ +==========================================+ BUTTON MANAGER +==========================================+ #
class ButtonManager:

    def create_bottom_buttons(container, submitcmd, clearentries, width=320, rely=0.5, infolabel=None):

        # Clear button functionality
        def clear_entries(entries=clearentries):
            for entry in entries: entry.delete(0, len(entry.get()))
            if infolabel:
                infolabel.place_forget() # Remove the infolabel

        # Frame to hold
        lowerframe = ctk.CTkFrame(container, fg_color='transparent')
        lowerframe.place(relx=0.5, rely=rely, anchor=CENTER)

        # Buttons
        submit = ctk.CTkButton(lowerframe,
               text='Submit',
               font=('ADLaM Display', 22, 'bold'),
               width=width,
               height=50,
               corner_radius=30,
               command=submitcmd)
        clear = ctk.CTkButton(lowerframe,
               text='Clear',
               font=('ADLaM Display', 22, 'bold'),
               width=width,
               height=50,
               corner_radius=30,
               command=clear_entries)
        submit.pack(side=LEFT, padx=10)
        clear.pack(side=RIGHT, padx=10)

    def create_back_button(container, main, infolabel):
        def go_back():
            main.show_frame(MainPage)
            if infolabel:
                infolabel.place_forget() # Remove the infolabel

        back = ctk.CTkButton(container,
            text='Back',
            font=('ADLaM Display', 22, 'bold'),
            width=80,
            height=50,
            corner_radius=30,
            command=go_back)
        back.place(relx=0.1, rely=0.1, anchor=CENTER)

#^ +============================================+ ENTRYPOINT +============================================+ #

if __name__ == "__main__":
    app = MainApp()
    app.geometry('1024x576')
    app.resizable(False, False)
    app.mainloop()