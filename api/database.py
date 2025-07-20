from pymongo import MongoClient

client=MongoClient("mongodb+srv://swamy:swamy718@cluster0.pp28wu1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client.todo
collection=db["todo_collection"]