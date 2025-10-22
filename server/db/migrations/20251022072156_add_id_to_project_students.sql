-- migrate:up

-- Add id column as primary key to project_students
-- First, drop the existing primary key constraint
ALTER TABLE project_students DROP CONSTRAINT project_students_pkey;

-- Add id column
ALTER TABLE project_students ADD COLUMN id SERIAL PRIMARY KEY;

-- Recreate unique constraint for project_id and student_id
ALTER TABLE project_students ADD CONSTRAINT project_students_unique UNIQUE (project_id, student_id);

-- migrate:down

-- Remove unique constraint
ALTER TABLE project_students DROP CONSTRAINT project_students_unique;

-- Remove id column
ALTER TABLE project_students DROP COLUMN id;

-- Restore original composite primary key
ALTER TABLE project_students ADD PRIMARY KEY (project_id, student_id);

