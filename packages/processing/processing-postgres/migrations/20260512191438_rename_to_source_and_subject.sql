-- migrate:up
ALTER TABLE conversions RENAME COLUMN lab_attempt_id TO source_id;
ALTER TABLE conversions RENAME COLUMN instructor_id TO subject_id;

-- migrate:down
ALTER TABLE conversions RENAME COLUMN source_id TO lab_attempt_id;
ALTER TABLE conversions RENAME COLUMN subject_id TO instructor_id;
