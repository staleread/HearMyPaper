-- migrate:up

ALTER TABLE users
  ADD COLUMN public_key BYTEA NOT NULL CHECK (octet_length(public_key) = 32);

-- migrate:down

ALTER TABLE users
  DROP COLUMN public_key;
