const express = require('express');
const app = express();
const port = 3000;

// Serve static files from the 'static' directory
app.use(express.static('static'));

// Endpoint for calculation
app.get('/calculate', (req, res) => {
    res.send('Result of 2*2 is ' + (2*2));
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
