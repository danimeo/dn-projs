import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import LineEditor from './components/LineEditor';
// const cors = require("cors");
// const express = require('express');
// const app = express();


// app.use(cors({
//   origin: 'http://localhost:5000', // Replace with your frontend URL
//   methods: ['GET', 'POST'], // Allow specific HTTP methods
//   allowedHeaders: ['Content-Type', 'Authorization'], // Allow specific headers
// }));


const App = () => {
  const [note, setNote] = useState('');
  const [lines, setLines] = useState([]);
  const [isSaving, setIsSaving] = useState(false);
  
  useEffect(() => {
    }, []);

  useEffect(() => {
    axios.get('http://localhost:5000/note')
      // .then(response => response.text())
      .then(text => {
        const linesArray = text.split('\n');
        setLines(linesArray);
      })
      .catch(error => console.error('Error reading the file:', error));
    // Fetch the existing note on mount
    axios.get('http://localhost:5000/api/note')
      .then(response => setNote(response.data.note))
      .catch(error => console.error('Error fetching note:', error));
  }, []);

  const handleSave = (index, newLine) => {
    const updatedLines = [...lines];
    updatedLines[index] = newLine;
    setLines(updatedLines);
  };

  const handleNoteChange = (value) => {
    setNote(value);
  };

  const saveNote = () => {
    setIsSaving(true);
    axios.post('http://localhost:5000/api/note', { note })
      .then(() => {
        alert('Note saved successfully!');
        setIsSaving(false);
      })
      .catch(error => {
        console.error('Error saving note:', error);
        setIsSaving(false);
      });
  };

  return (
    <div className="App">
      <h1>Note Editor</h1>
      <LineEditor lines={lines} onSave={handleSave} />
      <ReactQuill value={note} onChange={handleNoteChange} />
      <button onClick={saveNote} disabled={isSaving}>
        {isSaving ? 'Saving...' : 'Save Note'}
      </button>
    </div>
  );
};

export default App;
