-- migrate:up
CREATE TABLE conversions (
    conversion_id UUID PRIMARY KEY,
    lab_attempt_id UUID NOT NULL,
    instructor_id VARCHAR(75) NOT NULL,
    task_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- migrate:down
DROP TABLE IF EXISTS conversions;
