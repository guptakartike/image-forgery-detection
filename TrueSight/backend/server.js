const express = require('express');
const cors = require('cors');
const path = require('path');
const detectRoute = require('./routes/detect');

const app = express();
const PORT = Number(process.env.PORT || 8080);

app.use(cors());
app.use(express.json());

// Serve frontend files
app.use(express.static(path.join(__dirname, '../frontend')));

// API routes
app.use('/api', detectRoute);

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
