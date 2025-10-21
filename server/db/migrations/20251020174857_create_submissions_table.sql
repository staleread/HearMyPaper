-- migrate:up
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    content BYTEA NOT NULL
);

-- migrate:down
DROP TABLE submissions;
