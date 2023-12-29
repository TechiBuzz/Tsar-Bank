# DEBUGGING TOOL
# TO READ ACCOUNT DATA FROM FILE
# USE ONLY WHEN data.pkl IS PRESENT!
import pickle
with open('data.pkl', 'rb') as file:
    loaded_data = pickle.load(file)
print(loaded_data)