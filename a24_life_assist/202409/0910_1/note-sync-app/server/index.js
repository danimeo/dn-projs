const cors = require('cors');
const express = require('express');
const bodyParser = require('body-parser');
const simpleGit = require('simple-git');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 5000;
const git = simpleGit();
const noteFilePath = path.join(__dirname, 'note.txt');

app.use(bodyParser.json());

app.use(cors({
    origin: 'http://localhost:3000', // Replace with your frontend URL
    methods: ['GET', 'POST'], // Allow specific HTTP methods
    allowedHeaders: ['Content-Type', 'Authorization'], // Allow specific headers
  }));

// Serve static files from the React app
app.use(express.static(path.join(__dirname, '../build')));

// API routes
app.get('/api/note', (req, res) => {
  fs.readFile(noteFilePath, 'utf8', (err, data) => {
    if (err) return res.status(500).json({ error: 'Error reading note' });
    res.json({ note: data });
  });
});

app.post('/api/note', (req, res) => {
  const { note } = req.body;
  fs.writeFile(noteFilePath, note, 'utf8', (err) => {
    if (err) {
        console.log('Note file path:', noteFilePath);
        return res.status(500).json({ error: 'Error saving note' });
    }
    git.add(noteFilePath)
      .commit('Updated note')
      .push(['origin', 'main'])
      .then(() => res.json({ message: 'Note saved and pushed to Git!' }))
      .catch(() => res.status(500).json({ error: 'Error pushing note to Git' }));
  });
});

// Handle any other routes by serving the React app
// app.get('*', (req, res) => {
//     res.sendFile(path.join(__dirname, '../build/index.html'));
//   });
app.get('*', (req, res) => {
    console.log(__dirname);
    res.sendFile(path.join(__dirname, '../build/note.txt'));
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
