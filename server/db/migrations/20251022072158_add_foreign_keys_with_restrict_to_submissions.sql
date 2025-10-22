-- migrate:up

-- First, we need to add the project_student_id column to submissions table
ALTER TABLE submissions 
  ADD COLUMN project_student_id INTEGER NOT NULL REFERENCES project_students(id) ON DELETE RESTRICT;

-- Create index for better query performance
CREATE INDEX idx_submissions_project_student_id ON submissions(project_student_id);

-- migrate:down

DROP INDEX IF EXISTS idx_submissions_project_student_id;
ALTER TABLE submissions DROP COLUMN project_student_id;

