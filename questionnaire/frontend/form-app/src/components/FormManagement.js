import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FormManagement = ({ courseId }) => {
  const [forms, setForms] = useState([]);
  const [formTitle, setFormTitle] = useState('');

  useEffect(() => {
    // Fetch forms for a specific course
    axios.get(`http://localhost:8000/courses/${courseId}/forms`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => setForms(response.data))
      .catch(error => console.error('Error fetching forms:', error));
  }, [courseId]);

  const handleAddForm = () => {
    axios.post(`http://localhost:8000/courses/${courseId}/forms`, { title: formTitle }, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => {
        setForms([...forms, response.data]);
        setFormTitle('');
      })
      .catch(error => console.error('Error adding form:', error));
  };

  return (
    <div>
      <h2>Form Management</h2>
      <input 
        type="text" 
        value={formTitle} 
        onChange={(e) => setFormTitle(e.target.value)} 
        placeholder="Form Title" 
      />
      <button onClick={handleAddForm}>Add Form</button>
      <ul>
        {forms.map(form => (
          <li key={form.id}>{form.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default FormManagement;
