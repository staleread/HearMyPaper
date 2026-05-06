-- UP
CREATE TABLE users (
    id VARCHAR(75) PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    surname VARCHAR(75) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    public_key BYTEA NOT NULL,
    confidentiality_level VARCHAR(50) NOT NULL DEFAULT 'UNCLASSIFIED',
    integrity_levels VARCHAR(50)[] NOT NULL DEFAULT '{"UNCLASSIFIED"}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_name UNIQUE (name, surname)
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    instructor_id VARCHAR(75) NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE project_students (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    student_id VARCHAR(75) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(project_id, student_id)
);

CREATE TYPE transfer_status AS ENUM ('pending', 'uploaded', 'failed');

CREATE TABLE submissions (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_student_id INTEGER NOT NULL REFERENCES project_students(id) ON DELETE RESTRICT,
    storage_path TEXT NOT NULL,
    content_hash VARCHAR(64),
    status transfer_status DEFAULT 'pending',
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TYPE job_status AS ENUM ('queued', 'processing', 'completed', 'failed');

CREATE TABLE conversions (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID NOT NULL REFERENCES submissions(uuid) ON DELETE CASCADE,
    instructor_id VARCHAR(75) NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    input_path TEXT NOT NULL,
    output_path TEXT,
    status job_status DEFAULT 'queued',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- DOWN
DROP TABLE IF EXISTS conversions;
DROP TYPE IF EXISTS job_status;
DROP TABLE IF EXISTS submissions;
DROP TYPE IF EXISTS transfer_status;
DROP TABLE IF EXISTS project_students;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;
