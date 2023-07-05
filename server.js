const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = 3000;

app.post('/start', (req, res) => {
  exec('python3 sample.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python code: ${error}`);
      res.status(500).send('Internal Server Error');
    } else {
      console.log(`Python code output: ${stdout}`);
      res.status(200).json({ output: stdout }); // Sending output as JSON response
    }
  });
});


app.post('/enter', (req, res) => {
  exec('python3 -c "input(\'Press Enter to continue...\')"', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Enter command: ${error}`);
      res.status(500).send('Internal Server Error');
    } else {
      console.log(`Enter command executed successfully`);
      res.status(200).send('Enter command executed successfully');
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
