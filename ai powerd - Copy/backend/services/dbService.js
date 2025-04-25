const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { MongoClient } = require('mongodb');

// MongoDB Atlas connection string
const uri = 'mongodb+srv://jainanushk8:1QOc9z2qAt4AIA3F@clusterai-ml.0abossl.mongodb.net/ai_task_db?retryWrites=true&w=majority&appName=ClusterAI-ML'; // Replace with your MongoDB Atlas connection string
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

// Database and collection details
const dbName = 'dbTasksystem'; // Replace with your database name
const collectionName = 'AIproject'; // Replace with your collection name

// Path to the folder containing CSV files
const csvFolderPath = path.join(__dirname, 'data'); // Replace with your folder path

// Connect to MongoDB Atlas
async function connectToDB() {
  try {
    await client.connect();
    console.log('Connected to MongoDB Atlas');
    return client.db(dbName).collection(collectionName);
  } catch (err) {
    console.error('Error connecting to MongoDB', err);
  }
}

// Process a single CSV file
function processCSVFile(filePath, collection) {
  return new Promise((resolve, reject) => {
    const records = [];
    
    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (row) => {
        records.push(row); // Add each row from the CSV to the records array
      })
      .on('end', async () => {
        console.log(`Finished reading ${filePath}`);
        try {
          // Insert the CSV data into MongoDB
          await collection.insertMany(records);
          console.log(`Data from ${filePath} inserted successfully!`);
          resolve();
        } catch (err) {
          reject(`Error inserting data from ${filePath}: ${err}`);
        }
      })
      .on('error', (err) => {
        reject(`Error reading file ${filePath}: ${err}`);
      });
  });
}

// Main function to process all CSV files in the folder
async function processCSVFiles() {
  const collection = await connectToDB();
  
  if (!collection) {
    console.log('Failed to connect to the collection');
    return;
  }

  // Ensure that csvFolderPath is correct
  console.log('CSV Folder Path:', csvFolderPath);

  // Read all CSV files in the directory
  fs.readdir(csvFolderPath, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      return;
    }

    const csvFiles = files.filter((file) => path.extname(file) === '.csv');
    if (csvFiles.length === 0) {
      console.log('No CSV files found in the folder.');
      return;
    }

    // Process each CSV file
    csvFiles.forEach((file) => {
      const filePath = path.join(csvFolderPath, file);
      console.log('Processing file:', filePath); // Debugging: log the full path of the file
      processCSVFile(filePath, collection).catch((err) => {
        console.error(err);
      });
    });
  });
}

// Run the script
processCSVFiles().finally(() => {
  client.close(); // Close the connection when done
});
