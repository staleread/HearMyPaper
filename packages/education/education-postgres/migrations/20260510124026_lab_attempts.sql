-- migrate:up
CREATE TABLE lab_attempts (
    attempt_id UUID PRIMARY KEY,
    student_id VARCHAR(75) NOT NULL,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    submission_id UUID NOT NULL UNIQUE,
    submitted_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_on_time BOOLEAN NOT NULL,
    grade INTEGER,
    instructor_feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_lab_attempts_student_project ON lab_attempts(student_id, project_id);

-- migrate:down
DROP TABLE IF EXISTS lab_attempts;
