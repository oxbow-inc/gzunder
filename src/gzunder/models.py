"""Database ORM models."""
from tortoise import fields
from tortoise.models import Model


class Client(Model):
    """Telegram clients."""

    client_id = fields.IntField(pk=True)


class Meeting(Model):
    """Created meetings."""

    meeting_id = fields.IntField(pk=True)
    client = fields.ForeignKeyField("models.Client", related_name="meetings")
    title = fields.TextField()
    time_start = fields.DatetimeField(null=True)
    time_end = fields.DatetimeField(null=True)
    whoami = fields.TextField(default="")
    whoru = fields.TextField(default="")
    location = fields.TextField(default="")
    description = fields.TextField(default="")
    killed_at = fields.DatetimeField(null=True)


class Bot(Model):
    """Registered telegram bots."""

    bot_id = fields.IntField(pk=True)
    name = fields.TextField()  # ex.: `Playful Monkey`, `Sad Elephant`
    tg_key = fields.TextField()


class Dialog(Model):
    """Established dialogs."""

    dialog_id = fields.IntField(pk=True)
    client_from = fields.ForeignKeyField(
        "models.Client", related_name="dialogs_sent"
    )  # client.dialogs
    client_to = fields.ForeignKeyField(
        "models.Client", related_name="dialogs_rec"
    )
    meeting = fields.ForeignKeyField("models.Meeting", related_name="dialogs")
    bot = fields.ForeignKeyField("models.Bot", related_name="dialogs")


class Message(Model):
    """Messages running through bots."""

    msg_id = fields.IntField(pk=True)
    dialog = fields.ForeignKeyField("models.Dialog", related_name="messages")
    sender = fields.ForeignKeyField("models.Client", related_name="messages")
    text = fields.TextField()
