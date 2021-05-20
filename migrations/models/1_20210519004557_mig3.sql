-- upgrade --
ALTER TABLE "meeting" ADD "killed_at" TIMESTAMPTZ;
ALTER TABLE "meeting" DROP COLUMN "time_kill";
ALTER TABLE "meeting" DROP COLUMN "is_active";
-- downgrade --
ALTER TABLE "meeting" ADD "time_kill" TIMESTAMPTZ NOT NULL;
ALTER TABLE "meeting" ADD "is_active" BOOL NOT NULL  DEFAULT True;
ALTER TABLE "meeting" DROP COLUMN "killed_at";
