-- migrate:up
ALTER TABLE education.projects ADD COLUMN max_grade INTEGER NOT NULL DEFAULT 100;

-- migrate:down
ALTER TABLE education.projects DROP COLUMN max_grade;
