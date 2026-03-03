import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './styles.css';

console.log('Index.js loaded');
const rootElement = document.getElementById('root');
console.log('Root element:', rootElement);

if (rootElement) {
  const root = createRoot(rootElement);
  root.render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
  console.log('App rendered');
} else {
  console.error('Root element not found!');
}
