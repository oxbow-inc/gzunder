"""Create-Read-Update-Delete database operatoins."""
from typing import Iterator

from tortoise import run_async
from tortoise import Tortoise
from tortoise.models import Model
from tortoise.transactions import atomic

from gzunder.models import Client
from gzunder.models import Meeting
from gzunder.settings import settings
from gzunder.settings import TORTOISE_ORM


async def init() -> None:
    """Bootstrap DB."""
    # Connect to the database
    await Tortoise.init(config=TORTOISE_ORM)
    # Generate schema
    await Tortoise.generate_schemas()


@atomic()
async def create_meeting(client_id, **kwargs) -> None:
    """Insert a new meeting."""
    # Create client if not exists
    client, _ = await Client.get_or_create(client_id=client_id)
    # Create meeting
    await Meeting.create(client=client, **kwargs)


async def get_client_meetings(client_id) -> Iterator[Model]:
    """Get all meetings for certain client."""
    queryset = Meeting.filter(client=client_id)
    meetings = await queryset.all()
    return meetings


async def main():
    """Main function."""
    await init()
    await create_meeting(
        client_id=100,
        title="Фуколдианские чтения",  # смешное слово прост)
        time_start=None,
        time_end=None,
        whoami="Алиса Аспергер (она/ее), ЛГБТК+, квир, атеистка, веганесса",
        whoru="будь девушкой или не токсиком",
        location="у меня дома",
        description="Обсуждаем археологию знания, деконструируем печеньки. UwU",
    )
    await create_meeting(
        client_id=101,
        title="Могу оформить пушку",
        time_start=None,
        time_end=None,
        whoami="Борис Бритва. Russki weapon enthusiast",
        whoru="",
        location="закладкой",
        description="звонить по номеру [данные удалены] и договоримся",
    )
    await create_meeting(
        client_id=settings.tg_id_keril,
        title="Я тут просто чтобы заполнить пустоту в БД",
        time_start=None,
        time_end=None,
        whoami="Кырыл Керил - не пишите, не обижайте",
        whoru="",
        location="(_._)",
        description="Но что заполнит пустоту в моем сердце?",
    )
    await create_meeting(
        client_id=settings.tg_id_lesha,
        title="сурвив дуэль на пиццу",
        time_start=None,
        time_end=None,
        whoami="Леша (вы меня знаете)",
        whoru="",
        location="интернеты",
        description="на sv-98 + оружие по выбору.\nпроигравший дарит победителю 10% акций Папы Джонса.",
    )


if __name__ == "__main__":
    run_async(main())
