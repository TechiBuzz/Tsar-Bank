
#^ +=============================================+ IMPORTS +=============================================+ #

from tkinter import *
import customtkinter as ctk
from PIL import Image
import random
import pickle

#^ +=========================================+ CUSTOM TKINTER +==========================================+ #

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

#^ +===========================================+ GOD SECTION +===========================================+ #

# Main Account Storage
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
            pickle.dump({10000:{'name':'Example','password':'pass','age':70,'balance':5000}}, file)

#^ +============================================+ COMMON VARS +============================================+ #

common_width = 450
common_height = 55
common_labelfont = ('ADLaM Display', 40, 'bold')
common_entryfont = ('Bahnschrift Light', 32, 'bold')

#^ +============================================+ ENTRYPOINT +============================================+ #
class MainApp(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self) # Call super

        self.title('Tsar Bank')
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for Page in (MainPage, LoginPage, CreatePage, LoggedInPage, CreditPage, WithdrawPage, TransferPage):
            frame = Page(self.container, self)
            self.frames[Page] = frame # personal note - for each class assign a value of its instance
            frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(MainPage)

    def show_frame(self, container, *args):
        frame = self.frames[container]
        frame.tkraise()

        if args:
            frame.update_current_account(*args)
            
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

    def place_info_label(infolabel):
        infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)  # Call super

        # INFO THINGY
        infolabel = ctk.CTkLabel(self, text='Error!',font=('Bahnschrift Light', 22))

        # FRAME TO HOLD ALL
        boxframe = ctk.CTkFrame(self, fg_color='transparent', corner_radius=40)

        # LABELS
        accountnum_label = ctk.CTkLabel(boxframe, text='Account Number:', font=common_labelfont)
        accountnum_label.grid(row=0,column=0, padx=10, pady=8)

        password_label = ctk.CTkLabel(boxframe, text='Password:', font=common_labelfont)
        password_label.grid(row=1,column=0, padx=10, pady=8, sticky='w')

        # ENTRIES
        accountnum_entry = ctk.CTkEntry(boxframe, width=common_width, height=common_height, font=common_entryfont, corner_radius=50)
        accountnum_entry.grid(row=0,column=1, pady=8)

        password_entry = ctk.CTkEntry(boxframe, width=common_width, height=common_height, font=common_entryfont, show='*', corner_radius=50)
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
                LoginPage.place_info_label(infolabel)
            # Get password
            password = password_entry.get()

            # VALIDATION
            if valid_accnum:
                if password.isspace() or password == '':
                    infolabel.configure(text='⚠️ Account number or password field cannot be empty!')
                    LoginPage.place_info_label(infolabel)
                elif not AccountManager.accountnumber_exists(accnum):
                    infolabel.configure(text='⚠️ Account number not found!')
                    LoginPage.place_info_label(infolabel)
                elif not AccountManager.password_matches(accnum, password):
                    infolabel.configure(text='⚠️ Please enter the correct password!')
                    LoginPage.place_info_label(infolabel)
                else:
                    AccountManager.log_into_account(accnum, container)
                    accountnum_entry.delete(0, len(str(accnum)))
                    password_entry.delete(0, len(password))

        # CREATING SUBMIT AND CLEAR BUTTONS
        ButtonManager.create_bottom_buttons(self, submit_login, [accountnum_entry, password_entry], 320, 0.8, infolabel)

        # BACK BUTTON
        ButtonManager.create_back_button(self, container, infolabel, entries=[accountnum_entry, password_entry])

#^ +========================================+ CREATE ACCOUNT PAGE +========================================+ #
class CreatePage(ctk.CTkFrame):

    def place_info_label(infolabel):
        infolabel.place(relx=0.5, rely=0.65, anchor=CENTER)

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)  # Call super

        # INFO THINGY
        infolabel = ctk.CTkLabel(self, text='Error!',font=('Bahnschrift Light', 22))

        # FRAME TO HOLD ALL
        boxframe = ctk.CTkFrame(self, fg_color='transparent')

        # LABELS
        username_label = ctk.CTkLabel(boxframe, text='Username:', font=common_labelfont)
        username_label.grid(row=0,column=0, padx=10, pady=8)

        password_label = ctk.CTkLabel(boxframe, text='Password:', font=common_labelfont)
        password_label.grid(row=1,column=0, padx=10, pady=8, sticky='w')
        
        age_label = ctk.CTkLabel(boxframe, text='Age:', font=common_labelfont)
        age_label.grid(row=2,column=0, padx=10, pady=8, sticky='w')

        # ENTRIES
        username_entry = ctk.CTkEntry(boxframe, width=common_width, height=common_height, font=common_entryfont, corner_radius=50)
        username_entry.grid(row=0,column=1, pady=8)

        password_entry = ctk.CTkEntry(boxframe, width=common_width, height=common_height, font=common_entryfont, show='*', corner_radius=50)
        password_entry.grid(row=1,column=1, pady=8)
        
        age_entry = ctk.CTkEntry(boxframe, width=common_width, height=common_height, font=common_entryfont, corner_radius=50)
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
                CreatePage.place_info_label(infolabel)
            elif not is_valid_username(username):
                infolabel.configure(text='⚠️ Username cannot contain numbers!')
                CreatePage.place_info_label(infolabel)
            elif password.__contains__(' '):
                infolabel.configure(text='⚠️ Password cannot contain whitespaces!')
                CreatePage.place_info_label(infolabel)
            elif not age.isdigit():
                infolabel.configure(text='⚠️ Age must be an integer!')
                CreatePage.place_info_label(infolabel)
            elif not int(age) >= 18:
                infolabel.configure(text='⚠️ Minimum age to sign-up is 18 years!')
                CreatePage.place_info_label(infolabel)
            else:
                infolabel.place_forget() # Remove the error
            
                username_entry.delete(0, len(username)) # Clear username entry box
                password_entry.delete(0, len(password)) # Clear password entry box
                age_entry.delete(0, len(age)) # Clear age entry box

                # Create account and retrieve the account number
                accnum = AccountManager.create_new_account(username=username.strip().title(), password=password, age=age)

                infotext = 'You account has been successfully created! \n Your account number is: ' + str(accnum)
            
                infolabel.configure(text=infotext)
                infolabel.place(relx=0.5, rely=0.66, anchor=CENTER)

        # INFORMATICS
        info_icon = ctk.CTkImage(dark_image=Image.open('icons/info.png'))
        info = ctk.CTkLabel(self, 
                            text='  Please ensure the details are correct as once submitted they cannot be changed!',
                            font=('Bahnschrift Light', 16),
                            image=info_icon, compound=LEFT)
        info.place(relx=0.5, rely=0.9, anchor=CENTER)

        # CREATING SUBMIT AND CLEAR BUTTONS
        ButtonManager.create_bottom_buttons(self, submit_create, [username_entry, password_entry, age_entry], 320, 0.8, infolabel)     

        # BACK BUTTON
        ButtonManager.create_back_button(self, container, infolabel, entries=[username_entry, password_entry, age_entry])

#^ +==========================================+ LOGGED IN PAGE +===========================================+ #
class PageHelper:

    def create_box_page(textlabel ,master, container, submitcmd, two_boxes=False, secondtextlabel = '', infolabel=None):

        master.text = ctk.CTkLabel(master, width=600, height=70, font=('ADLaM Display', 45, 'bold'), corner_radius=50, text=textlabel)
        master.text.place(relx=0.5, rely=0.34, anchor=CENTER)

        master.entrybox = ctk.CTkEntry(master, width=600, height=70, font=common_entryfont, corner_radius=50)
        master.entrybox.place(relx=0.5, rely=0.46, anchor=CENTER)

        master.infolabel = ctk.CTkLabel(master, text='Error!',font=('Bahnschrift Light', 26))

        entries = [master.entrybox]

        if two_boxes:
            master.text.configure(width=400)
            master.text.place(relx=0.27, rely=0.35, anchor=CENTER)
            master.entrybox.configure(width=400)
            master.entrybox.place(relx=0.65, rely=0.35, anchor=CENTER) # change pos of 1st box

            master.text2 = ctk.CTkLabel(master, width=400, height=70, font=('ADLaM Display', 45, 'bold'), corner_radius=50, text=secondtextlabel)
            master.text2.place(relx=0.23, rely=0.5, anchor=CENTER)

            master.entrybox2 = ctk.CTkEntry(master, width=400, height=70, font=common_entryfont, corner_radius=50)
            master.entrybox2.place(relx=0.65, rely=0.5, anchor=CENTER)

            entries.append(master.entrybox2)

        ButtonManager.create_bottom_buttons(master, submitcmd, entries, rely=0.8, width=290, infolabel=master.infolabel)
        ButtonManager.create_back_button(master, container, master.infolabel, entries=entries, page_to_go=LoggedInPage)

class CreditPage(ctk.CTkFrame):

    def place_info_label(infolabel):
        infolabel.place(relx=0.5, rely=0.625, anchor=CENTER)

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)

        self.text = self.entrybox = self.infolabel = self.current_account = None

        def submit_credit():
            credit_amt = self.entrybox.get()
            infolabel = self.infolabel

            if not credit_amt.isdigit():
                infolabel.configure(text='⚠️ Credit amount must be an integer!')
                CreditPage.place_info_label(infolabel)
            else:
                self.entrybox.delete(0, len(credit_amt)) # Clear entrybox

                new_balance = self.current_account['balance'] + int(credit_amt)
                self.current_account.update({'balance':new_balance})
                
                with open('data.pkl', 'wb') as file:
                    pickle.dump(accounts, file)

                container.frames[LoggedInPage].update_balance_label(new_balance)

                success_text = '✅ Successfully credited $ ' + credit_amt + '\n New Balance is: $ ' + str(self.current_account['balance'])
                infolabel.configure(text=success_text)
                CreditPage.place_info_label(infolabel)

        PageHelper.create_box_page('Enter amount to credit:',self, container, submit_credit, self.infolabel)

    # Set account number for session
    def update_current_account(self, accnum): self.current_account = accounts[accnum]

class WithdrawPage(ctk.CTkFrame):

    def place_info_label(infolabel):
        infolabel.place(relx=0.5, rely=0.625, anchor=CENTER)

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)

        self.text = self.entrybox = self.infolabel = self.current_account = None

        def submit_withdraw():
            credit_amt = self.entrybox.get()
            infolabel = self.infolabel

            if not credit_amt.isdigit():
                infolabel.configure(text='⚠️ Withdraw amount must be a positive integer!')
                WithdrawPage.place_info_label(infolabel)
            elif int(credit_amt) == 0:
                infolabel.configure(text='⚠️ Minimum withdrawal is of $ 1!')
                WithdrawPage.place_info_label(infolabel)
            elif self.current_account['balance'] < int(credit_amt):
                infolabel.configure(text='⚠️ Not enought balance in account!')
                WithdrawPage.place_info_label(infolabel)
            else:
                self.entrybox.delete(0, len(credit_amt)) # Clear entrybox

                new_balance = self.current_account['balance'] - int(credit_amt)
                self.current_account.update({'balance':new_balance})
                
                with open('data.pkl', 'wb') as file:
                    pickle.dump(accounts, file)

                container.frames[LoggedInPage].update_balance_label(new_balance)

                success_text = '✅ Successfully debited $ ' + credit_amt + '\n New Balance is: $ ' + str(self.current_account['balance'])
                infolabel.configure(text=success_text)
                WithdrawPage.place_info_label(infolabel)
        
        PageHelper.create_box_page('Enter amount to withdraw:',self, container, submit_withdraw, self.infolabel)

    # Set account number for session
    def update_current_account(self, accnum): self.current_account = accounts[accnum]

class TransferPage(ctk.CTkFrame):

    def place_info_label(infolabel):
        infolabel.place(relx=0.5, rely=0.64, anchor=CENTER)

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)

        self.text = self.entrybox = self.infolabel = self.current_account = self.entrybox2 = None

        def submit_transfer():
            transfer_to = self.entrybox.get()
            transfer_amt = self.entrybox2.get()
            infolabel = self.infolabel

            if not transfer_amt.isdigit() or not transfer_to.isdigit(): # handles negatives and blank text also
                infolabel.configure(text='⚠️ Transfer amount must be a positive integer!')
                TransferPage.place_info_label(infolabel)
            elif int(transfer_amt) == 0:
                infolabel.configure(text='⚠️ Minimum transaction is of $ 1!')
                TransferPage.place_info_label(infolabel)
            elif not AccountManager.accountnumber_exists(int(transfer_to)):
                infolabel.configure(text='⚠️ Receiver account not found!')
                TransferPage.place_info_label(infolabel)
            elif self.current_account['balance'] < int(transfer_amt):
                infolabel.configure(text='⚠️ Not enought balance in account!')
                TransferPage.place_info_label(infolabel)
            else:
                self.entrybox.delete(0, len(transfer_to)) # Clear entrybox
                self.entrybox2.delete(0, len(transfer_amt)) # Clear entrybox
                

                new_balance = self.current_account['balance'] - int(transfer_amt)
                self.current_account.update({'balance':new_balance})
                
                their_account = accounts[int(transfer_to)]

                their_new_balance = their_account['balance'] + int(transfer_amt)
                their_account.update({'balance':their_new_balance})

                with open('data.pkl', 'wb') as file:
                    pickle.dump(accounts, file)

                container.frames[LoggedInPage].update_balance_label(new_balance)

                success_text = '✅ Successfully transfered $ ' + transfer_amt + ' to ' + their_account['name'] + '\n New Balance is: $ ' + str(self.current_account['balance'])
                infolabel.configure(text=success_text)
                infolabel.place(relx=0.5, rely=0.64, anchor=CENTER)
        
        PageHelper.create_box_page('Account No:', self, container, submit_transfer, True,'Amount:', self.infolabel)

    # Set account number for session
    def update_current_account(self, accnum): self.current_account = accounts[accnum]

class LoggedInPage(ctk.CTkFrame):

    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)
        self.current_account = self.current_account_number = None  # No account selected as of instantiation

        # COMMONS
        width = 600
        height = 60
        buttonfont = ('ADLaM Display', 27, 'bold')

        # BACK BUTTON
        ButtonManager.create_back_button(self, container, page_to_go=MainPage)

        # USERNAME LABEL
        self.username_label = ctk.CTkLabel(self,
                                          text='',
                                          font=('ADLaM Display', 45, 'bold'),
                                          image=ctk.CTkImage(dark_image=Image.open('icons/user.png'), size=(120,120)), compound=TOP)
        self.username_label.place(relx=0.5, rely=0.22, anchor=CENTER)

        # BALANCE LABEL
        self.balance_label = ctk.CTkLabel(self,
                                          text='',
                                          font=('ADLaM Display', 45, 'bold'))
        self.balance_label.place(relx=0.5, rely=0.45, anchor=CENTER)

        # CREDIT BUTTON
        credit = ctk.CTkButton(self,
                               text='Credit Money',
                               font=buttonfont,
                               width=width,
                               height=height,
                               corner_radius=30,
                               command=lambda: container.show_frame(CreditPage, self.current_account_number))
        credit.place(relx=0.5, rely=0.59, anchor=CENTER)

        # WITHDRAW BUTTON
        withdraw = ctk.CTkButton(self,
                              text='Withdraw Money',
                              font=buttonfont,
                              width=width,
                              height=height,
                              corner_radius=30,
                              command=lambda: container.show_frame(WithdrawPage, self.current_account_number))
        withdraw.place(relx=0.5, rely=0.72, anchor=CENTER)

        # TRANSFER BUTTON
        transfer = ctk.CTkButton(self,
                                 text='Transfer Money',
                                 font=buttonfont,
                                 width=width,
                                 height=height,
                                 corner_radius=30,
                                 command=lambda: container.show_frame(TransferPage, self.current_account_number))
        transfer.place(relx=0.5, rely=0.84, anchor=CENTER)

    def update_current_account(self, accnum):
        self.current_account_number = accnum
        self.current_account = accounts[accnum]
        self.update_balance_label(self.current_account['balance'])  # Call the method to update balance label
        self.update_username_label(self.current_account['name']) # Call the method to update name label

    def update_balance_label(self, new_balance):
        if self.current_account and 'balance' in self.current_account:
            balance_text = 'Current Balance: $ ' + str(new_balance)
            self.balance_label.configure(text=balance_text)

    def update_username_label(self, new_username):
        if self.current_account and 'name' in self.current_account:
            username_text = str(new_username).title()
            self.username_label.configure(text=username_text)

#^ +==========================================+ ACCOUNT MANAGER +==========================================+ #
class AccountManager:

    # Method to create new account (its self explanatory)
    def create_new_account(username, password, age) -> int:
        # Create random account number
        accountnumber = random.randint(10000, 99999)
        while accountnumber in accounts.keys(): # Make sure account number is unique
            accountnumber = random.randint(10000, 99999)

        # Update dictionaty and file
        accounts.update({accountnumber : {'name':username,'password':password,'age':age,'balance':0}})
        with open('data.pkl', 'wb') as file:
            pickle.dump(accounts, file)

        return accountnumber
    
    # Helper methods
    def log_into_account(accnum :int, container):
        container.show_frame(LoggedInPage, accnum)
        
    def accountnumber_exists(accnum :int):
        return True if accnum in accounts.keys() else False
        
    def password_matches(accnum, password):
        return True if accounts[accnum]['password'] == password else False
    
#^ +==========================================+ BUTTON MANAGER +==========================================+ #
class ButtonManager:

    # CREATE SUBMIT AND CLEAR BUTTON
    def create_bottom_buttons(container, submitcmd, clearentries=[], width=320, rely=0.5, infolabel=None):

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

    # CREATE BACK BUTTON
    def create_back_button(container, main, infolabel=None, entries=[], page_to_go=MainPage):
        def go_back(page=page_to_go):
            main.show_frame(page)
            for entry in entries: entry.delete(0, len(entry.get()))
            if infolabel:
                infolabel.place_forget() # Remove the infolabel

        back = ctk.CTkButton(container,
            text='⬅',
            font=('ADLaM Display', 25, 'bold'),
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
