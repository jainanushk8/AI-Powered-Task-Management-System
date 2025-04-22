// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Optional for styles
import App from './App'; // Import the App component
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // This is the root div in your index.html
);

reportWebVitals();
