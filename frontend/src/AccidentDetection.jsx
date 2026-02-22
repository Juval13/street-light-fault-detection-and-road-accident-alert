import React, { useState } from 'react';
import './styles.css';

export default function AccidentDetection() {
  // Example data, replace with real data as needed
  const [accidents] = useState([
    { id: 1, details: 'Car collision at Main St.', ambulance: 'Yes' },
    { id: 2, details: 'Bike accident at 2nd Ave.', ambulance: 'No' },
    { id: 3, details: 'Truck overturned at Highway 5.', ambulance: 'Yes' },
  ]);

  return (
    <div className="accident-detection-container">
      <div className="accident-detection-card">
        <h2>Accident Detection</h2>
        <table className="accident-table">
          <thead>
            <tr>
              <th>No</th>
              <th>Accident</th>
              <th>Inform Ambulance</th>
            </tr>
          </thead>
          <tbody>
            {accidents.map((accident, idx) => (
              <tr key={accident.id}>
                <td>{idx + 1}</td>
                <td>{accident.details}</td>
                <td>{accident.ambulance}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
