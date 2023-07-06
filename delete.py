import pymongo

# MongoDB connection string
connection_string = "mongodb+srv://unipolar:12345@cluster0.dhy44zc.mongodb.net/"
#connection_string = "mongodb://localhost:27017"

# Connect to MongoDB
client = pymongo.MongoClient(connection_string)

# Access the first database
database1 = client["bse_listed_stocks"]

# Access the second database
database2 = client["nse_listed_stocks"]

# Keep the latest 10 documents and delete the rest in database1
for collection_name in database1.list_collection_names():
    collection = database1[collection_name]
    latest_documents = collection.find({}, sort=[("_id", pymongo.DESCENDING)], limit=10)
    latest_ids = [doc["_id"] for doc in latest_documents]
    result = collection.delete_many({"_id": {"$nin": latest_ids}})
    count = result.deleted_count
    print(f"Deleted {count} documents from {collection_name} in database1.")

# Keep the latest 10 documents and delete the rest in database2
for collection_name in database2.list_collection_names():
    collection = database2[collection_name]
    latest_documents = collection.find({}, sort=[("_id", pymongo.DESCENDING)], limit=10)
    latest_ids = [doc["_id"] for doc in latest_documents]
    result = collection.delete_many({"_id": {"$nin": latest_ids}})
    count = result.deleted_count
    print(f"Deleted {count} documents from {collection_name} in database2.")

print("Deletion completed.")
