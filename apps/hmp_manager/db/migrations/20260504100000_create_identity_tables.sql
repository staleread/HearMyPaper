-- UP
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    p_uuid UUID UNIQUE DEFAULT gen_random_uuid(), -- Pseudonym for Zero Trust flows
    pseudonym VARCHAR(100) UNIQUE NOT NULL,       -- Adjective-noun-number identifier
    name VARCHAR(75) NOT NULL,
    surname VARCHAR(75) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    public_key BYTEA NOT NULL, -- User's X25519/Ed25519 key
    confidentiality_level INTEGER NOT NULL DEFAULT 0, -- 0: Unclassified, 1: Restricted, etc.
    integrity_levels INTEGER[] NOT NULL DEFAULT '{0}', -- List of levels user can "Write" to
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_name UNIQUE (name, surname)
);

CREATE INDEX idx_users_pseudonym ON users(pseudonym);

CREATE TABLE service_identities (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL UNIQUE, -- e.g., 'hmp_tts'
    spiffe_id VARCHAR(255) NOT NULL UNIQUE,   -- Verification via SPIRE
    public_key BYTEA NOT NULL,                -- For Instructor -> Service Sealed Box
    last_rotated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- DOWN
DROP TABLE service_identities;
DROP TABLE users;
