"""
MongoDB Connection Test Script
Tests the connection to MongoDB and verifies database setup
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import sys

# MongoDB Configuration (Authenticated)
MONGODB_URI = 'mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin'
DB_NAME = 'bloodsmear'

def test_mongodb_connection():
    """Test MongoDB connection and database setup"""
    print("=" * 60)
    print("MongoDB Connection Test")
    print("=" * 60)
    
    try:
        # Attempt to connect to MongoDB
        print(f"\n1. Connecting to MongoDB at: {MONGODB_URI}")
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        print("2. Testing connection...")
        client.admin.command('ping')
        print("   ✓ Successfully connected to MongoDB!")
        
        # Access the database
        print(f"\n3. Accessing database: {DB_NAME}")
        db = client[DB_NAME]
        
        # List existing collections
        collections = db.list_collection_names()
        print(f"   ✓ Database accessed successfully")
        print(f"   Existing collections: {collections if collections else 'None (database is empty)'}")
        
        # Create collections if they don't exist
        print("\n4. Verifying required collections...")
        required_collections = ['users', 'analyses', 'results']
        
        for collection_name in required_collections:
            if collection_name not in collections:
                db.create_collection(collection_name)
                print(f"   ✓ Created collection: {collection_name}")
            else:
                print(f"   ✓ Collection exists: {collection_name}")
        
        # Test write operation
        print("\n5. Testing write operation...")
        test_collection = db['test_connection']
        test_doc = {'test': 'connection', 'status': 'success'}
        result = test_collection.insert_one(test_doc)
        print(f"   ✓ Write test successful (ID: {result.inserted_id})")
        
        # Test read operation
        print("6. Testing read operation...")
        retrieved_doc = test_collection.find_one({'_id': result.inserted_id})
        print(f"   ✓ Read test successful: {retrieved_doc}")
        
        # Clean up test document
        test_collection.delete_one({'_id': result.inserted_id})
        print("   ✓ Cleanup completed")
        
        # Display database stats
        print("\n7. Database Statistics:")
        for collection_name in required_collections:
            count = db[collection_name].count_documents({})
            print(f"   - {collection_name}: {count} documents")
        
        print("\n" + "=" * 60)
        print("✓ All tests passed! MongoDB is ready to use.")
        print("=" * 60)
        
        return True
        
    except ConnectionFailure:
        print("\n✗ ERROR: Could not connect to MongoDB")
        print("  Make sure MongoDB is running on localhost:27017")
        print("\n  To start MongoDB:")
        print("  1. Open MongoDB Compass and connect to mongodb://localhost:27017/")
        print("  2. Or run: net start MongoDB (requires admin)")
        return False
        
    except ServerSelectionTimeoutError:
        print("\n✗ ERROR: MongoDB server is not responding")
        print("  Make sure MongoDB service is running")
        print("\n  To start MongoDB:")
        print("  1. Open MongoDB Compass and connect to mongodb://localhost:27017/")
        print("  2. Or run: net start MongoDB (requires admin)")
        return False
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return False
    
    finally:
        try:
            client.close()
            print("\nConnection closed.")
        except:
            pass

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
