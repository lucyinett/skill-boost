from pymongo import MongoClient

def check_mongodb_connection(connection_string, database_name, collection_name):
    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        db = client[database_name]

        # Check if the collection exists
        if collection_name in db.list_collection_names():
            print(f"Connected to MongoDB collection: {collection_name}")
        else:
            print(f"Collection {collection_name} not found in the database.")

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

if __name__ == "__main__":
    # Replace these values with your MongoDB connection details
    mongodb_connection_string = "mongodb+srv://skillset:ny-1HSames021@cluster0.rcms5tl.mongodb.net/"
    database_name = "skill-set-db"
    collection_name = "skill-data"

    check_mongodb_connection(mongodb_connection_string, database_name, collection_name)
