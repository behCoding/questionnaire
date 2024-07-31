import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ username: '', password: '', role: '' });

  useEffect(() => {
    axios.get('http://localhost:8000/users', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => setUsers(response.data))
      .catch(error => console.error('Error fetching users:', error));
  }, []);

  const handleAddUser = () => {
    axios.post('http://localhost:8000/users', newUser, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => {
        setUsers([...users, response.data]);
        setNewUser({ username: '', password: '', role: '' });
      })
      .catch(error => console.error('Error adding user:', error));
  };

  const handleDeleteUser = (userId) => {
    axios.delete(`http://localhost:8000/users/${userId}`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(() => setUsers(users.filter(user => user.id !== userId)))
      .catch(error => console.error('Error deleting user:', error));
  };

  return (
    <div>
      <h2>User Management</h2>
      <input 
        type="text" 
        placeholder="Username" 
        value={newUser.username} 
        onChange={(e) => setNewUser({ ...newUser, username: e.target.value })} 
      />
      <input 
        type="password" 
        placeholder="Password" 
        value={newUser.password} 
        onChange={(e) => setNewUser({ ...newUser, password: e.target.value })} 
      />
      <input 
        type="text" 
        placeholder="Role" 
        value={newUser.role} 
        onChange={(e) => setNewUser({ ...newUser, role: e.target.value })} 
      />
      <button onClick={handleAddUser}>Add User</button>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            {user.username} - {user.role}
            <button onClick={() => handleDeleteUser(user.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserManagement;
