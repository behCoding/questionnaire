import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TeacherDashboard = () => {
  const [forms, setForms] = useState([]);
  const [newForm, setNewForm] = useState({ name: '' });

  useEffect(() => {
    axios.get('http://localhost:8000/forms', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => setForms(response.data))
      .catch(error => console.error('Error fetching forms:', error));
  }, []);

  const handleAddForm = () => {
    axios.post('http://localhost:8000/forms', newForm, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => {
        setForms([...forms, response.data]);
        setNewForm({ name: '' });
      })
      .catch(error => console.error('Error adding form:', error));
  };

  const handleDeleteForm = (formId) => {
    axios.delete(`http://localhost:8000/forms/${formId}`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(() => setForms(forms.filter(form => form.id !== formId)))
      .catch(error => console.error('Error deleting form:', error));
  };

  return (
    <div>
      <h2>Teacher Dashboard</h2>
      <input 
        type="text" 
        placeholder="Form Name" 
        value={newForm.name} 
        onChange={(e) => setNewForm({ ...newForm, name: e.target.value })} 
      />
      <button onClick={handleAddForm}>Add Form</button>
      <ul>
        {forms.map(form => (
          <li key={form.id}>
            {form.name}
            <button onClick={() => handleDeleteForm(form.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TeacherDashboard;
