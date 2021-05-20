-- upgrade --
CREATE TABLE IF NOT EXISTS "bot" (
    "bot_id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "tg_key" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "user_id" SERIAL NOT NULL PRIMARY KEY,
    "current_context" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "meeting" (
    "meeting_id" SERIAL NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "time_start" TIMESTAMPTZ,
    "time_end" TIMESTAMPTZ,
    "whoami" TEXT NOT NULL,
    "whoru" TEXT NOT NULL,
    "location" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "killed_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "user" ("user_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "dialog" (
    "dialog_id" SERIAL NOT NULL PRIMARY KEY,
    "bot_id" INT NOT NULL REFERENCES "bot" ("bot_id") ON DELETE CASCADE,
    "user_to_id" INT NOT NULL REFERENCES "user" ("user_id") ON DELETE CASCADE,
    "user_from_id" INT NOT NULL REFERENCES "user" ("user_id") ON DELETE CASCADE,
    "meeting_id" INT NOT NULL REFERENCES "meeting" ("meeting_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "message" (
    "msg_id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "dialog_id" INT NOT NULL REFERENCES "dialog" ("dialog_id") ON DELETE CASCADE,
    "sender_id" INT NOT NULL REFERENCES "user" ("user_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
