-- migrate:up

CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  syllabus_summary TEXT NOT NULL,
  description TEXT NOT NULL,
  instructor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  deadline VARCHAR(50) NOT NULL, -- ISO string format
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_students (
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (project_id, student_id)
);

-- Create indexes for better performance
CREATE INDEX idx_projects_instructor_id ON projects(instructor_id);
CREATE INDEX idx_projects_deadline ON projects(deadline);
CREATE INDEX idx_project_students_project_id ON project_students(project_id);
CREATE INDEX idx_project_students_student_id ON project_students(student_id);

-- migrate:down

DROP TABLE project_students;
DROP TABLE projects;
