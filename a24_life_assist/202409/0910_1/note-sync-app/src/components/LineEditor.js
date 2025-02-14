import React, { useState } from 'react';

const LineEditor = ({ lines, onSave }) => {
  const [editingIndex, setEditingIndex] = useState(null);
  const [editedLine, setEditedLine] = useState('');

  const handleEditClick = (index) => {
    setEditingIndex(index);
    setEditedLine(lines[index]);
  };

  const handleSaveClick = () => {
    onSave(editingIndex, editedLine);
    setEditingIndex(null);
    setEditedLine('');
  };

  return (
    <div>
      <ul>
        {lines.map((line, index) => (
          <li key={index}>
            {editingIndex === index ? (
              <div>
                <input
                  type="text"
                  value={editedLine}
                  onChange={(e) => setEditedLine(e.target.value)}
                />
                <button onClick={handleSaveClick}>Save</button>
              </div>
            ) : (
              <div>
                {line}
                <button onClick={() => handleEditClick(index)}>Edit</button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LineEditor;
