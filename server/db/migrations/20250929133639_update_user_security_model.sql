-- migrate:up

ALTER TABLE users
  RENAME COLUMN access_level TO confidentiality_level;

ALTER TABLE users
  DROP COLUMN access_rules,
  ADD COLUMN integrity_levels INTEGER[] NOT NULL DEFAULT '{}';

-- migrate:down

ALTER TABLE users
  RENAME COLUMN confidentiality_level TO access_level;

ALTER TABLE users
  DROP COLUMN integrity_levels,
  ADD COLUMN access_rules VARCHAR(125)[] NOT NULL DEFAULT '{}';