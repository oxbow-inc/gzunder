from tortoise import Tortoise, run_async


async def init():
    # Connect to the database
    await Tortoise.init(
        db_url="postgres://postgres:secret@localhost:5432/stage",
        modules={"models": ["gzunder.models"]},
    )
    # Generate schema
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init())
