-- migrate:up

ALTER TABLE action_logs
  ADD COLUMN user_id INTEGER REFERENCES users(id);

-- migrate:down

ALTER TABLE action_logs
  DROP COLUMN user_id;
