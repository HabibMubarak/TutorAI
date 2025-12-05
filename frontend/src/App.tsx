import { useEffect, useState } from 'react';

function App() {
  const [status, setStatus] = useState<string>("Lade...");

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then(response => response.json())
      .then(data => {
        setStatus(data.message);          // <--- Zeigt ALLES an, egal wie es heißt
      })
      .catch(error => setStatus("Fehler: " + error));
  }, []);

  return (
    <div style={{ padding: '50px', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h1>TutorAI System Check</h1>
      <hr />
      <h2>Backend Status:</h2>
      {/* Wenn das hier grün wird, haben sich Frontend und Backend geküsst */}
      <p style={{ fontSize: '24px', color: 'green', fontWeight: 'bold' }}>
        {status}
      </p>
    </div>
  );
}

export default App;