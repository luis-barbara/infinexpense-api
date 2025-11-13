FROM python:3.12-slim

RUN pip install poetry

COPY . .

RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

RUN poetry install

# Add entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

WORKDIR /app/
EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
