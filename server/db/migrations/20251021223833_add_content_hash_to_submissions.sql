-- migrate:up
ALTER TABLE submissions ADD COLUMN content_hash VARCHAR(32);

-- migrate:down
ALTER TABLE submissions DROP COLUMN content_hash;
