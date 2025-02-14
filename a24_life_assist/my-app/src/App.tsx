import React from 'react';
// import logo from './logo.svg';
import './App.css';
import MonthViewCalendar from './components/MonthViewCalendar';
import MyForm from './components/MyForm';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p> */}
        <div className='title'><p><strong>📅Calendar</strong></p></div>
        <p className='subtitle'>Danim's First React App</p>
      </header>
        <MonthViewCalendar />
        {/* <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Danim's First React App
        </a> */}
        <h2>临时服药记录提交器</h2>
        <MyForm />
    </div>
  );
}

export default App;
