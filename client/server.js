
// Set SendGrid API Key
//sgMail.setApiKey('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');

const express = require('express');
const bodyParser = require('body-parser');
const sgMail = require('@sendgrid/mail');
const cors = require('cors'); // Import the CORS middleware

const { Storage } = require('@google-cloud/storage');
const { exec } = require('child_process');

// Initialize the app
const app = express();

// Enable CORS for all routes
app.use(cors()); 

app.use(bodyParser.json()); // To handle JSON requests

// Set your SendGrid API key
sgMail.setApiKey('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'); // Replace with your actual API key

//---------GET THE URLS FROM THE CLOUD------

// Google Cloud Storage setup
const storage = new Storage();
const bucketName = 'my_baldi';
const fileName = 'download_urls.json';

// Function to retrieve URLs from Google Cloud Storage
async function getDownloadUrlsFromGCloud() {
    const bucket = storage.bucket(bucketName);
    const file = bucket.file(fileName);

    // Read the file content
    const data = await file.download();
    const urls = JSON.parse(data);

    return urls.download_urls;
}

//----------GET THE URLS FROM THE CLOUD

function runPythonScript() {
    exec('python3 server/landsat.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error}`);
            return;
        }
        console.log(`Python Script Output: ${stdout}`);
        if (stderr) {
            console.error(`Python Script Error Output: ${stderr}`);
        }
    });
}

// Run Python script when the server starts
runPythonScript();

// Endpoint to send email
app.post('/send-email', (req, res) => {
    const { email, lat, lng } = req.body;

    // Construct the email message
    const msg = {
        to: email,
        from: 'faizluqman7@gmail.com', // Replace with your verified SendGrid sender email
        subject: 'Coordinates Selected',
        text: `Coordinates selected by the user: Latitude: ${lat}, Longitude: ${lng}`,
        html: `<strong>Coordinates selected: Latitude: ${lat}, Longitude: ${lng}</strong>`,
    };

    // Send the email
    sgMail
        .send(msg)
        .then(() => {
            res.status(200).send('Email sent successfully');
        })
        .catch((error) => {
            console.error(error);
            res.status(500).send('Error sending email');
        });
});
// DELETE IF NOT WORKING
// Endpoint to handle satellite data retrieval request
app.post('/retrieve-satellite-data', (req, res) => {
    const { lat, lng } = req.body;

    const { exec } = require('child_process');
    const command = `python3 landsat.py ${lat} ${lng}`;  // Call landsat.py with coordinates as arguments

    // Execute the Python script
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing landsat.py: ${error}`);
            return res.status(500).send('Failed to retrieve satellite data');
        }
        res.status(200).send(`Satellite data retrieval started with lat: ${lat}, lng: ${lng}`);
    });
});

// Run the server
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
