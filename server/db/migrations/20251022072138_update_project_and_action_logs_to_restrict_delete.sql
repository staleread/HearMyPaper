-- migrate:up

-- Update projects table: Change instructor_id foreign key from CASCADE to RESTRICT
ALTER TABLE projects 
  DROP CONSTRAINT projects_instructor_id_fkey,
  ADD CONSTRAINT projects_instructor_id_fkey 
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE RESTRICT;

-- Update project_students table: Change project_id foreign key from CASCADE to RESTRICT
ALTER TABLE project_students 
  DROP CONSTRAINT project_students_project_id_fkey,
  ADD CONSTRAINT project_students_project_id_fkey 
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE RESTRICT;

-- Update project_students table: Change student_id foreign key from CASCADE to RESTRICT
ALTER TABLE project_students 
  DROP CONSTRAINT project_students_student_id_fkey,
  ADD CONSTRAINT project_students_student_id_fkey 
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE RESTRICT;

-- Update action_logs table: Change user_id foreign key to RESTRICT (it had no ON DELETE clause)
ALTER TABLE action_logs 
  DROP CONSTRAINT action_logs_user_id_fkey,
  ADD CONSTRAINT action_logs_user_id_fkey 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;

-- migrate:down

-- Revert projects table: Change instructor_id foreign key from RESTRICT to CASCADE
ALTER TABLE projects 
  DROP CONSTRAINT projects_instructor_id_fkey,
  ADD CONSTRAINT projects_instructor_id_fkey 
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE CASCADE;

-- Revert project_students table: Change project_id foreign key from RESTRICT to CASCADE
ALTER TABLE project_students 
  DROP CONSTRAINT project_students_project_id_fkey,
  ADD CONSTRAINT project_students_project_id_fkey 
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;

-- Revert project_students table: Change student_id foreign key from RESTRICT to CASCADE
ALTER TABLE project_students 
  DROP CONSTRAINT project_students_student_id_fkey,
  ADD CONSTRAINT project_students_student_id_fkey 
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE;

-- Revert action_logs table: Remove ON DELETE RESTRICT
ALTER TABLE action_logs 
  DROP CONSTRAINT action_logs_user_id_fkey,
  ADD CONSTRAINT action_logs_user_id_fkey 
    FOREIGN KEY (user_id) REFERENCES users(id);

