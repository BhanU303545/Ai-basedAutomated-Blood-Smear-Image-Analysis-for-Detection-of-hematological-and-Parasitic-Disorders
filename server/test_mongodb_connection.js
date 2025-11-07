/**
 * MongoDB Connection Test Script (Node.js)
 * Tests the connection to MongoDB and verifies database setup
 */

const { MongoClient } = require('mongodb');

// MongoDB Configuration (Authenticated)
const MONGODB_URI = 'mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin';
const DB_NAME = 'bloodsmear';

async function testMongoDBConnection() {
    console.log('='.repeat(60));
    console.log('MongoDB Connection Test (Node.js)');
    console.log('='.repeat(60));

    let client;

    try {
        // Attempt to connect to MongoDB
        console.log(`\n1. Connecting to MongoDB at: ${MONGODB_URI}`);
        client = new MongoClient(MONGODB_URI, {
            useUnifiedTopology: true,
            serverSelectionTimeoutMS: 5000
        });

        await client.connect();
        console.log('   ✓ Successfully connected to MongoDB!');

        // Access the database
        console.log(`\n2. Accessing database: ${DB_NAME}`);
        const db = client.db(DB_NAME);
        console.log('   ✓ Database accessed successfully');

        // List existing collections
        const collections = await db.listCollections().toArray();
        const collectionNames = collections.map(c => c.name);
        console.log(`   Existing collections: ${collectionNames.length > 0 ? collectionNames.join(', ') : 'None (database is empty)'}`);

        // Verify required collections
        console.log('\n3. Verifying required collections...');
        const requiredCollections = ['users', 'analyses', 'results'];

        for (const collectionName of requiredCollections) {
            if (!collectionNames.includes(collectionName)) {
                await db.createCollection(collectionName);
                console.log(`   ✓ Created collection: ${collectionName}`);
            } else {
                console.log(`   ✓ Collection exists: ${collectionName}`);
            }
        }

        // Test write operation
        console.log('\n4. Testing write operation...');
        const testCollection = db.collection('test_connection');
        const testDoc = { test: 'connection', status: 'success', timestamp: new Date() };
        const insertResult = await testCollection.insertOne(testDoc);
        console.log(`   ✓ Write test successful (ID: ${insertResult.insertedId})`);

        // Test read operation
        console.log('5. Testing read operation...');
        const retrievedDoc = await testCollection.findOne({ _id: insertResult.insertedId });
        console.log(`   ✓ Read test successful:`, retrievedDoc);

        // Clean up test document
        await testCollection.deleteOne({ _id: insertResult.insertedId });
        console.log('   ✓ Cleanup completed');

        // Display database stats
        console.log('\n6. Database Statistics:');
        for (const collectionName of requiredCollections) {
            const count = await db.collection(collectionName).countDocuments({});
            console.log(`   - ${collectionName}: ${count} documents`);
        }

        console.log('\n' + '='.repeat(60));
        console.log('✓ All tests passed! MongoDB is ready to use.');
        console.log('='.repeat(60));

        return true;

    } catch (error) {
        console.error('\n✗ ERROR:', error.message);
        console.log('\nMake sure MongoDB is running on localhost:27017');
        console.log('\nTo start MongoDB:');
        console.log('1. Open MongoDB Compass and connect to mongodb://localhost:27017/');
        console.log('2. Or run: net start MongoDB (requires admin)');
        return false;

    } finally {
        if (client) {
            await client.close();
            console.log('\nConnection closed.');
        }
    }
}

// Run the test
testMongoDBConnection()
    .then(success => {
        process.exit(success ? 0 : 1);
    })
    .catch(error => {
        console.error('Unexpected error:', error);
        process.exit(1);
    });
