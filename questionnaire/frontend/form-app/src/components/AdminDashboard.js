import React from 'react';

function AdminDashboard() {
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <div>
        <a href="/manage-courses">Manage Courses</a>
      </div>
      <div>
        <a href="/manage-users">Manage Users</a>
      </div>
    </div>
  );
}

export default AdminDashboard;
