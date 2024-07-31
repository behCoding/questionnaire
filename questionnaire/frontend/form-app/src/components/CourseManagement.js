import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CourseManagement = () => {
  const [courses, setCourses] = useState([]);
  const [courseName, setCourseName] = useState('');

  useEffect(() => {
    // Fetch courses on component mount
    axios.get('http://localhost:8000/courses')
      .then(response => setCourses(response.data))
      .catch(error => console.error('Error fetching courses:', error));
  }, []);

  const handleAddCourse = () => {
    axios.post('http://localhost:8000/courses', { name: courseName }, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(response => {
        setCourses([...courses, response.data]);
        setCourseName('');
      })
      .catch(error => console.error('Error adding course:', error));
  };

  return (
    <div>
      <h2>Course Management</h2>
      <input 
        type="text" 
        value={courseName} 
        onChange={(e) => setCourseName(e.target.value)} 
        placeholder="Course Name" 
      />
      <button onClick={handleAddCourse}>Add Course</button>
      <ul>
        {courses.map(course => (
          <li key={course.id}>{course.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CourseManagement;
