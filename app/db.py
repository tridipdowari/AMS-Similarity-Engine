from pymongo import MongoClient

MONGO_URI = "mongodb+srv://AMS-DB-USER:AMS-123@cluster0.qkrtn8a.mongodb.net"

client = MongoClient(MONGO_URI)

db = client["test"]

collection = db["projects"]