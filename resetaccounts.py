import pickle
with open('data.pkl', 'wb') as file:
    pickle.dump({1000:{'name':'example','password':'examplepassword','age':69}}, file)