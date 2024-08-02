import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FormManagement from './FormManagement';

const TeacherDashboard = () => {
  const [allCourses, setAllCourses] = useState([]);
  const [teacherCourses, setTeacherCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [showForms, setShowForms] = useState(null); // Track which course's forms to show

  // Retrieve user from localStorage and parse it
  const teacherId = localStorage.getItem('user_id');

  useEffect(() => {
    if (!teacherId) {
      console.error("User is not logged in or user information is missing.");
      return;
    }

    // Fetch all courses
    axios.get('http://localhost:8000/courses/all', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => setAllCourses(response.data))
      .catch(error => console.error('Error fetching all courses:', error));

    // Fetch teacher's courses
    axios.get(`http://localhost:8000/teachers/${teacherId}/courses`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => setTeacherCourses(response.data))
      .catch(error => console.error('Error fetching teacher courses:', error));
  }, [teacherId]);

  const handleAddCourse = () => {
    if (!selectedCourse) {
      console.error("No course selected.");
      return;
    }

    axios.post(`http://localhost:8000/teachers/${teacherId}/courses/${selectedCourse}`, {}, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => {
        setTeacherCourses([...teacherCourses, response.data]);
        setSelectedCourse('');
      })
      .catch(error => console.error('Error adding course to teacher:', error));
  };

  if (!teacherId) {
    return <div>Please log in to view your dashboard.</div>;
  }

  return (
    <div>
      <h2>Teacher Dashboard</h2>
      <div>
        <h3>All Courses</h3>
        <select value={selectedCourse} onChange={(e) => setSelectedCourse(e.target.value)}>
          <option value="">Select a course</option>
          {allCourses.map(course => (
            <option key={course.id} value={course.id}>{course.name}</option>
          ))}
        </select>
        <button onClick={handleAddCourse}>Add Course</button>
      </div>
      <div>
        <h3>My Courses</h3>
        <ul>
          {teacherCourses.map(course => (
            <li key={course.id}>
              {course.name}
              <button onClick={() => setShowForms(course.id)}>Manage Forms</button>
            </li>
          ))}
        </ul>
      </div>
      {showForms && <FormManagement courseId={showForms} />}
    </div>
  );
};

export default TeacherDashboard;
