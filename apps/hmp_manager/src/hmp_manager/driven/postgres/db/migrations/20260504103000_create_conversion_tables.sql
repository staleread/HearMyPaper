-- UP
CREATE TYPE job_status AS ENUM ('queued', 'processing', 'completed', 'failed');

CREATE TABLE conversions (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    instructor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    input_path TEXT NOT NULL,  -- Instructor re-encrypted Sealed Box for TTS
    output_path TEXT,          -- Path to the final encrypted Audio in MinIO
    status job_status DEFAULT 'queued',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit Trail (Append-Only)
CREATE TABLE action_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    actor_spiffe_id VARCHAR(255), -- Logs if a service (SVID) performed the action
    actor_pseudonym VARCHAR(100), -- Human-readable pseudonym for curators
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    is_success BOOLEAN NOT NULL,
    context JSONB -- Stores IP, User-Agent, or OPA decision metadata
);

-- DOWN
DROP TABLE action_logs;
DROP TABLE conversions;
DROP TYPE job_status;
