BEGIN;

CREATE TABLE "user" (
  id                    SERIAL,
  email_id              TEXT NOT NULL,
  name                  TEXT NOT NULL,
  password              TEXT NOT NULL,
  auth_token            TEXT,
  created               TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
ALTER TABLE "user" ADD CONSTRAINT user_email_id_key UNIQUE (email_id);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bingo;

COMMIT;
