FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

RUN poetry install --no-root

# Add entrypoint script to a location that won't be overwritten
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
