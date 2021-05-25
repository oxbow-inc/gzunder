-- upgrade --
CREATE TABLE IF NOT EXISTS "bot" (
    "bot_id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "tg_key" TEXT NOT NULL
);
COMMENT ON TABLE "bot" IS 'Registered telegram bots.';
CREATE TABLE IF NOT EXISTS "client" (
    "client_id" SERIAL NOT NULL PRIMARY KEY
);
COMMENT ON TABLE "client" IS 'Telegram clients.';
CREATE TABLE IF NOT EXISTS "meeting" (
    "meeting_id" SERIAL NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "time_start" TIMESTAMP,
    "time_end" TIMESTAMP,
    "whoami" TEXT NOT NULL,
    "whoru" TEXT NOT NULL,
    "location" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "killed_at" TIMESTAMP,
    "client_id" INT NOT NULL REFERENCES "client" ("client_id") ON DELETE CASCADE
);
COMMENT ON TABLE "meeting" IS 'Created meetings.';
CREATE TABLE IF NOT EXISTS "dialog" (
    "dialog_id" SERIAL NOT NULL PRIMARY KEY,
    "client_to_id" INT NOT NULL REFERENCES "client" ("client_id") ON DELETE CASCADE,
    "bot_id" INT NOT NULL REFERENCES "bot" ("bot_id") ON DELETE CASCADE,
    "meeting_id" INT NOT NULL REFERENCES "meeting" ("meeting_id") ON DELETE CASCADE,
    "client_from_id" INT NOT NULL REFERENCES "client" ("client_id") ON DELETE CASCADE
);
COMMENT ON TABLE "dialog" IS 'Established dialogs.';
CREATE TABLE IF NOT EXISTS "message" (
    "msg_id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "dialog_id" INT NOT NULL REFERENCES "dialog" ("dialog_id") ON DELETE CASCADE,
    "sender_id" INT NOT NULL REFERENCES "client" ("client_id") ON DELETE CASCADE
);
COMMENT ON TABLE "message" IS 'Messages running through bots.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
