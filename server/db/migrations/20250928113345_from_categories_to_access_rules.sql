-- migrate:up

ALTER TABLE users
  DROP COLUMN categories,
  ADD COLUMN access_rules VARCHAR(125)[] NOT NULL DEFAULT '{}';

-- migrate:down

ALTER TABLE users
  DROP COLUMN access_rules,
  ADD COLUMN categories VARCHAR(75)[] NOT NULL;

