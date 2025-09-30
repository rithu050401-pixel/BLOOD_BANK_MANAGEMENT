// server.js
const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const dbFile = path.join(__dirname, 'appointments.db');
const db = new sqlite3.Database(dbFile);

// Create table if not exists
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullName TEXT,
    age INTEGER,
    bloodGroup TEXT,
    phone TEXT,
    email TEXT,
    appointmentDate TEXT,
    comments TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
});

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname)); // Serve HTML, CSS, JS from same folder

// Handle form submission
app.post('/submit_appointment', (req, res) => {
  const { fullName, age, bloodGroup, phone, email, appointmentDate, comments } = req.body;

  // Validation
  if (!fullName || !age || age < 18 || !bloodGroup || !phone || !email || !appointmentDate) {
    return res.status(400).send('Missing or invalid fields');
  }

  // Insert into DB
  const stmt = db.prepare(`INSERT INTO appointments 
    (fullName, age, bloodGroup, phone, email, appointmentDate, comments) 
    VALUES (?, ?, ?, ?, ?, ?, ?)`);
  
  stmt.run(fullName, age, bloodGroup, phone, email, appointmentDate, comments || '', function(err) {
    if (err) return res.status(500).send('Database error: ' + err.message);
    res.redirect('/thanks.html'); // redirect after success
  });
  stmt.finalize();
});

// Start server
app.listen(3000, () => console.log('✅ Server running at http://localhost:3000'));
