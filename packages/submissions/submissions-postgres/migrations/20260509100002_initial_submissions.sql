-- migrate:up
CREATE TABLE submissions (
    submission_id UUID PRIMARY KEY,
    student_id VARCHAR(75) NOT NULL,
    project_id UUID NOT NULL,
    storage_path TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_submissions_project_id ON submissions (project_id);
CREATE INDEX idx_submissions_student_project ON submissions (student_id, project_id);

-- migrate:down
DROP TABLE submissions;
