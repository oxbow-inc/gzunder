from tortoise import Tortoise, run_async


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    # await Tortoise.init(
    #     db_url='sqlite://db.sqlite3',
    #     modules={'models': ['core.db']}
    # )
    await Tortoise.init(
        db_url='postgres://postgres:secret@localhost:5432/stage',
        modules={'models': ['core.db']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(init())
