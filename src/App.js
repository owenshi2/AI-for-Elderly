import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  const handleStart = async () => {
    try {
      const response = await fetch('/start', { method: 'POST' });
      const data = await response.json();
      console.log('Python code executed successfully');
      console.log('Output:', data.output); // Accessing the output from the response
    } catch (error) {
      console.error('Error executing Python code:', error);
    }
  };
  

  const handleEnter = async () => {
    try {
      await fetch('/enter', { method: 'POST' });
      setMessage('successfully press enter');
    } catch (error) {
      setMessage('Error executing Python code: ' + error);
    }
  };

  return (
    <div className="App">
      <button onClick={handleStart}>Run Python Code</button>
      <p>{message}</p>
      <button onClick={handleEnter}>Press Enter</button>
      <p>{message}</p>
    </div>
  );
}

export default App;

