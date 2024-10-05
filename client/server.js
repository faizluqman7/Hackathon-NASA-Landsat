
// Set SendGrid API Key
//sgMail.setApiKey('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');

const express = require('express');
const bodyParser = require('body-parser');
const sgMail = require('@sendgrid/mail');
const cors = require('cors'); // Import the CORS middleware

// Initialize the app
const app = express();

// Enable CORS for all routes
app.use(cors()); 

app.use(bodyParser.json()); // To handle JSON requests

// Set your SendGrid API key
sgMail.setApiKey('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'); // Replace with your actual API key

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

// Run the server
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
