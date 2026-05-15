import os

from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Mongo URI from .env
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB connection
client = MongoClient(MONGO_URI)

# Database and collection
db = client["test2"]

collection = db["projects"]