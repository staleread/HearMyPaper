-- migrate:up
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    instructor_id VARCHAR(75) NOT NULL,
    deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE project_students (
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    student_id VARCHAR(75) NOT NULL,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (project_id, student_id)
);

-- migrate:down
DROP TABLE IF EXISTS project_students;
DROP TABLE IF EXISTS projects;
