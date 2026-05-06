-- UP
CREATE TYPE transfer_status AS ENUM ('pending', 'uploaded', 'verified', 'failed');

CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    p_uuid UUID DEFAULT gen_random_uuid(), -- Used for the MinIO path: submissions/{p_uuid}/...
    project_student_id INTEGER NOT NULL REFERENCES project_students(id) ON DELETE RESTRICT,
    storage_path TEXT NOT NULL, -- MinIO path: e.g., 'submissions/2026/proj1/file.enc'
    content_hash VARCHAR(64),   -- SHA-256 of the encrypted box
    status transfer_status DEFAULT 'pending',
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- DOWN
DROP TABLE submissions;
DROP TYPE transfer_status;
