-- migrate:up

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(75) NOT NULL UNIQUE,
  access_level INTEGER NOT NULL,
  categories VARCHAR(75)[] NOT NULL
);

-- migrate:down

DROP TABLE users;
