import pickle
with open("tasks.pkl", "rb") as file:
    data = pickle.load(file)
    print(data)