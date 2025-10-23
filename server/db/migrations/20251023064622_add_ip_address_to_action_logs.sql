-- migrate:up

ALTER TABLE action_logs ADD COLUMN ip_address VARCHAR(45);

-- migrate:down

ALTER TABLE action_logs DROP COLUMN ip_address;
