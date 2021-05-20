from tortoise.models import Model
from tortoise import fields


class User(Model):
    user_id = fields.IntField(pk=True)
    current_context = fields.TextField()  # whatever


class Meeting(Model):
    meeting_id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="meetings")
    title = fields.TextField()
    time_start = fields.DatetimeField(null=True)
    time_end = fields.DatetimeField(null=True)
    whoami = fields.TextField(default="")
    whoru = fields.TextField(default="")
    location = fields.TextField(default="")
    description = fields.TextField(default="")
    killed_at = fields.DatetimeField(null=True)


class Bot(Model):
    bot_id = fields.IntField(pk=True)
    name = fields.TextField()  # ex.: `Playful Monkey`, `Sad Elephant`
    tg_key = fields.TextField()


class Dialog(Model):
    dialog_id = fields.IntField(pk=True)
    user_from = fields.ForeignKeyField(
        "models.User", related_name="dialogs_sent"
    )  # user.dialogs
    user_to = fields.ForeignKeyField("models.User", related_name="dialogs_rec")
    meeting = fields.ForeignKeyField("models.Meeting", related_name="dialogs")
    bot = fields.ForeignKeyField("models.Bot", related_name="dialogs")


class Message(Model):
    msg_id = fields.IntField(pk=True)
    dialog = fields.ForeignKeyField("models.Dialog", related_name="messages")
    sender = fields.ForeignKeyField("models.User", related_name="messages")
    text = fields.TextField()
