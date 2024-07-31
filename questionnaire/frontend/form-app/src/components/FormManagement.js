import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FormManagement = ({ courseId }) => {
  const [forms, setForms] = useState([]);
  const [formName, setFormName] = useState('');

  useEffect(() => {
    // Fetch forms for a specific course
    axios.get(`http://localhost:8000/courses/${courseId}/forms`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => setForms(response.data))
      .catch(error => console.error('Error fetching forms:', error));
  }, [courseId]);

  const handleAddForm = () => {
    axios.post(`http://localhost:8000/courses/${courseId}/forms`, { name: formName }, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => {
        setForms([...forms, response.data]);
        setFormName('');
      })
      .catch(error => console.error('Error adding form:', error));
  };

  return (
    <div>
      <h2>Form Management</h2>
      <input 
        type="text" 
        value={formName} 
        onChange={(e) => setFormName(e.target.value)} 
        placeholder="Form Name" 
      />
      <button onClick={handleAddForm}>Add Form</button>
      <ul>
        {forms.map(form => (
          <li key={form.id}>{form.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default FormManagement;
