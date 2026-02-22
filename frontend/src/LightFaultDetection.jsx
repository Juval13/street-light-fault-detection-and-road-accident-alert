import React, { useState } from 'react';
import './styles.css';

export default function LightFaultDetection() {
  // Example data, replace with real data as needed
  const [faults] = useState([
    { id: 1, fault: 'Blinking', answer: 2, fuses: 'Yes', informed: 'Yes' },
    { id: 2, fault: 'Not working', answer: 1, fuses: 'No', informed: 'No' },
    { id: 3, fault: 'Dim light', answer: 3, fuses: 'Yes', informed: 'Yes' },
  ]);

  return (
    <div className="light-fault-detection-container">
      <div className="light-fault-detection-card">
        <h2>Light Fault Detection</h2>
        <table className="light-fault-table">
          <thead>
            <tr>
              <th>No</th>
              <th>Light Fault</th>
              <th>Answer</th>
              <th>Fuses</th>
              <th>Informed</th>
            </tr>
          </thead>
          <tbody>
            {faults.map((fault, idx) => (
              <tr key={fault.id}>
                <td>{idx + 1}</td>
                <td>{fault.fault}</td>
                <td>{fault.answer}</td>
                <td>{fault.fuses}</td>
                <td>{fault.informed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
