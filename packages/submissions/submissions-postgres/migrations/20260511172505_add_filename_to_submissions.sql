-- migrate:up
ALTER TABLE submissions ADD COLUMN filename TEXT;
ALTER TABLE submissions ADD COLUMN extension TEXT;

-- migrate:down
ALTER TABLE submissions DROP COLUMN filename;
ALTER TABLE submissions DROP COLUMN extension;
