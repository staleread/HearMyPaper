-- migrate:up

-- Split username into name and surname, add email and expires_at
ALTER TABLE users 
  ADD COLUMN name VARCHAR(75),
  ADD COLUMN surname VARCHAR(75), 
  ADD COLUMN email VARCHAR(255),
  ADD COLUMN expires_at TIMESTAMP;

-- Migrate existing username data - split by space if possible
UPDATE users 
SET 
  name = CASE 
    WHEN position(' ' in username) > 0 
    THEN split_part(username, ' ', 1)
    ELSE username
  END,
  surname = CASE 
    WHEN position(' ' in username) > 0 
    THEN split_part(username, ' ', 2)
    ELSE username
  END,
  email = CONCAT(
    LOWER(
      CASE 
        WHEN position(' ' in username) > 0 
        THEN CONCAT(split_part(username, ' ', 1), '.', split_part(username, ' ', 2))
        ELSE CONCAT(username, '.', username)
      END
    ), 
    '@example.com'
  ),
  expires_at = CURRENT_TIMESTAMP + INTERVAL '1 year'; -- default expiry

-- Now make the new columns NOT NULL and add constraints
ALTER TABLE users 
  ALTER COLUMN name SET NOT NULL,
  ALTER COLUMN surname SET NOT NULL,
  ALTER COLUMN email SET NOT NULL,
  ALTER COLUMN expires_at SET NOT NULL;

-- Add email uniqueness constraint
ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE (email);

-- Add name+surname uniqueness constraint
ALTER TABLE users ADD CONSTRAINT users_name_surname_unique UNIQUE (name, surname);

-- Drop the old username column
ALTER TABLE users DROP COLUMN username;

-- migrate:down

-- Add back username column
ALTER TABLE users ADD COLUMN username VARCHAR(75);

-- Recreate username from name and surname
UPDATE users SET username = CONCAT(name, ' ', surname);

-- Make username NOT NULL and UNIQUE
ALTER TABLE users 
  ALTER COLUMN username SET NOT NULL,
  ADD CONSTRAINT users_username_unique UNIQUE (username);

-- Drop the new columns and constraints
ALTER TABLE users 
  DROP CONSTRAINT users_email_unique,
  DROP CONSTRAINT users_name_surname_unique,
  DROP COLUMN name,
  DROP COLUMN surname,
  DROP COLUMN email,
  DROP COLUMN expires_at;