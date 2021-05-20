TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:secret@localhost:5432/stage"
    },
    "apps": {
        "models": {
            "models": ["gzunder.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
