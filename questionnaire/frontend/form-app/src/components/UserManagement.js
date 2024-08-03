import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CourseManagement = () => {
  const [courses, setCourses] = useState([]);
  const [courseName, setCourseName] = useState('');
  const [editingCourse, setEditingCourse] = useState(null);

  useEffect(() => {
    // Fetch courses on component mount
    axios.get('http://localhost:8000/courses', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => setCourses(response.data))
      .catch(error => console.error('Error fetching courses:', error.response ? error.response.data : error.message));
  }, []);

  const handleAddCourse = () => {
    if (courseName.trim() === '') return;

    axios.post('http://localhost:8000/courses', { name: courseName }, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => {
        setCourses([...courses, response.data]);
        setCourseName('');
      })
      .catch(error => console.error('Error adding course:', error.response ? error.response.data : error.message));
  };

  const handleUpdateCourse = (courseId) => {
    if (courseName.trim() === '') return;

    axios.put(`http://localhost:8000/courses/${courseId}`, { name: courseName }, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => {
        const updatedCourses = courses.map(course => course.id === courseId ? response.data : course);
        setCourses(updatedCourses);
        setCourseName('');
        setEditingCourse(null);
      })
      .catch(error => console.error('Error updating course:', error.response ? error.response.data : error.message));
  };

  const handleDeleteCourse = (courseId) => {
    axios.delete(`http://localhost:8000/courses/${courseId}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(() => {
        setCourses(courses.filter(course => course.id !== courseId));
      })
      .catch(error => console.error('Error deleting course:', error.response ? error.response.data : error.message));
  };

  const startEditingCourse = (course) => {
    setCourseName(course.name);
    setEditingCourse(course.id);
  };

  return (
    <div>
      <h2>Course Management</h2>
      <div>
        <input 
          type="text" 
          value={courseName} 
          onChange={(e) => setCourseName(e.target.value)} 
          placeholder="Course Name" 
        />
        <button onClick={editingCourse ? () => handleUpdateCourse(editingCourse) : handleAddCourse}>
          {editingCourse ? 'Update Course' : 'Add Course'}
        </button>
        {editingCourse && (
          <button onClick={() => { setCourseName(''); setEditingCourse(null); }}>
            Cancel
          </button>
        )}
      </div>
      <ul>
        {courses.map(course => (
          <li key={course.id}>
            {course.name}
            <button onClick={() => startEditingCourse(course)}>Edit</button>
            <button onClick={() => handleDeleteCourse(course.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CourseManagement;
