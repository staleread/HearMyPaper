-- migrate:up

CREATE TABLE action_logs (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  action VARCHAR(60) NOT NULL,
  is_success BOOLEAN NOT NULL,
  reason TEXT
);

CREATE OR REPLACE FUNCTION prevent_action_logs_modification()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Modification of action_logs is not allowed';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER block_action_logs_update
  BEFORE UPDATE ON action_logs
  FOR EACH ROW
  EXECUTE FUNCTION prevent_action_logs_modification();

CREATE TRIGGER block_action_logs_delete
  BEFORE DELETE ON action_logs
  FOR EACH ROW
  EXECUTE FUNCTION prevent_action_logs_modification();

-- migrate:down

DROP TRIGGER IF EXISTS block_action_logs_delete ON action_logs;
DROP TRIGGER IF EXISTS block_action_logs_update ON action_logs;
DROP FUNCTION IF EXISTS prevent_action_logs_modification();
DROP TABLE IF EXISTS action_logs;
