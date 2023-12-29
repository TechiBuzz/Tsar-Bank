import pickle
import customtkinter as tk

# DEBUGGING TOOL
# TO READ ACCOUNT DATA FROM FILE
# USE ONLY WHEN data.pkl IS PRESENT!
loaded_data = {}

# Console Log
with open('data.pkl', 'rb') as file:
    loaded_data = pickle.load(file)

window = tk.CTk()
window.geometry("700x500")
window.title("Account Details")

header = tk.CTkLabel(window, text='Debug Account Data', font=("Monstressat Black", 40, "bold"), height=70)
header.pack()

frame = tk.CTkFrame(window)
frame.pack()

# Create headers
headers = ["Account Number", "Name", "Password", "Age", "Balance"]
for col, header in enumerate(headers):
    header_label = tk.CTkLabel(frame, text=header, font=("Monstressat Black", 26, "bold"))
    header_label.grid(row=0, column=col, padx=15, pady=15)

# Display account details in a tabular format
for row, (account_number, details) in enumerate(loaded_data.items(), start=1):
    tk.CTkLabel(frame, text=account_number, font=('Space Grotesk', 17)).grid(row=row, column=0, padx=5, pady=5)
    for col, value in enumerate(details.values(), start=1):
        tk.CTkLabel(frame, text=str(value), font=('Space Grotesk', 17)).grid(row=row, column=col, padx=5, pady=5)

window.mainloop()
