-- UP
CREATE TABLE users (
    id VARCHAR(75) PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    surname VARCHAR(75) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    public_key BYTEA NOT NULL,
    confidentiality_level VARCHAR(50) NOT NULL DEFAULT 'UNCLASSIFIED',
    integrity_levels VARCHAR(50)[] NOT NULL DEFAULT '{"UNCLASSIFIED"}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_name UNIQUE (name, surname)
);

-- DOWN
DROP TABLE IF EXISTS users;
