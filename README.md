


## Development

### Sources:
* [aerich tutorial](https://www.programmersought.com/article/46386196535/)

### Technical Decisions

#### [Beartype](https://github.com/beartype/beartype) vs [Pydantic](https://github.com/samuelcolvin/pydantic)
Pydantic has some mypy [issues](https://github.com/samuelcolvin/pydantic/issues/156), but it is still better,
as beartype does not have [application-level types](https://github.com/beartype/beartype/blob/main/beartype/vale/__init__.py#L47).

### Bootstrap
Requires `pyenv`, `pipx`, `poetry`, `docker-compose`, `git-secret`.

Then:
```sh
# Install python version
pyenv install 3.8.6

# Clone project and cd into it
git clone git@github.com:oxbow-inc/gzunder.git
cd gzunder

# Install project
poetry install -E fmt

# Run database
docker-compose rm -f pg_db; docker-compose up pg_db

# Initialization
# Creates
# * aerich.ini
# * migrations/...
poetry run aerich init -t gzunder.settings.TORTOISE_ORM
# Creates DB
poetry run aerich init-db

# Decrypt .env
git secret reveal
```
