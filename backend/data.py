from pymongo import MongoClient
import pandas as pd


# Load csv dataset
data = pd.read_csv('pokeapi.csv')

# Connect to MongoDB
client = MongoClient("mongodb+srv://<username>:<project-name>@cluster0.k0ch4.mongodb.net/myFirstDatabase"
                     "?retryWrites=true&w=majority")

db = client['pokeapi']
collection = db['pokeapi-pokemon']

data.reset_index(inplace=True)
data_dict = data.to_dict("records")

# Insert collection
collection.insert_many(data_dict)
