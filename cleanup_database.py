"""
Database Cleanup Script
This script removes invalid analysis records from MongoDB
"""

from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB (Authenticated)
client = MongoClient('mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin')
db = client['bloodsmear']
analyses_collection = db['analyses']

print("Starting database cleanup...")
print("=" * 50)

# Count total analyses before cleanup
total_before = analyses_collection.count_documents({})
print(f"Total analyses before cleanup: {total_before}")

# Find invalid analyses (missing result.predicted_class or result.confidence)
invalid_analyses = list(analyses_collection.find({
    '$or': [
        {'result': {'$exists': False}},
        {'result.predicted_class': {'$exists': False}},
        {'result.confidence': {'$exists': False}}
    ]
}))

print(f"Found {len(invalid_analyses)} invalid analyses")

if len(invalid_analyses) > 0:
    print("\nInvalid analyses:")
    for analysis in invalid_analyses:
        print(f"  - ID: {analysis.get('analysis_id', 'N/A')}")
        print(f"    Created: {analysis.get('created_at', 'N/A')}")
        print(f"    Result: {analysis.get('result', 'Missing')}")
        print()

    # Ask for confirmation
    response = input("Do you want to delete these invalid analyses? (yes/no): ")
    
    if response.lower() == 'yes':
        # Delete invalid analyses
        result = analyses_collection.delete_many({
            '$or': [
                {'result': {'$exists': False}},
                {'result.predicted_class': {'$exists': False}},
                {'result.confidence': {'$exists': False}}
            ]
        })
        
        print(f"\n✅ Deleted {result.deleted_count} invalid analyses")
        
        # Count total analyses after cleanup
        total_after = analyses_collection.count_documents({})
        print(f"Total analyses after cleanup: {total_after}")
    else:
        print("\n❌ Cleanup cancelled")
else:
    print("\n✅ No invalid analyses found. Database is clean!")

# Show remaining valid analyses
print("\n" + "=" * 50)
print("Valid analyses in database:")
valid_analyses = list(analyses_collection.find({}, {'_id': 0}).sort('created_at', -1).limit(10))

for analysis in valid_analyses:
    result = analysis.get('result', {})
    print(f"  - {result.get('predicted_class', 'N/A')} ({result.get('confidence', 0)*100:.1f}%)")
    print(f"    Created: {analysis.get('created_at', 'N/A')}")
    print()

print("=" * 50)
print("Cleanup complete!")
