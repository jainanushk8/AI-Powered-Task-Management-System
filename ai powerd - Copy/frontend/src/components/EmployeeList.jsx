import React, { useState, useEffect } from "react";

function EmployeeList() {
  const [employees, setEmployees] = useState([
    { id: 1, name: "John Doe", role: "Developer", proficiency: 8, experience: 5 },
    { id: 2, name: "Jane Smith", role: "Designer", proficiency: 7, experience: 4 },
  ]);

  return (
    <div className="employee-list">
      <h4>Employees</h4>
      <ul>
        {employees.map((employee) => (
          <li key={employee.id}>
            <strong>{employee.name}</strong> - {employee.role}
            <br />
            Proficiency: {employee.proficiency} / 10 | Experience: {employee.experience} years
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EmployeeList;
