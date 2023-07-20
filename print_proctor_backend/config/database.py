from pymongo import MongoClient

client = MongoClient("mongodb+srv://gc0300273:gxXppQDR6vnPE07h@cluster0.krmj5ky.mongodb.net/?retryWrites=true&w=majority")

db = client.print_practor

collection_name = db["users"]


