FROM python:3.12-slim

RUN pip install poetry

COPY . .

RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

RUN poetry install --no-root

# Create uploads directories with proper permissions
RUN mkdir -p /app/uploads/products /app/uploads/receipts && \
    chmod -R 755 /app/uploads

# Add entrypoint script to a location that won't be overwritten
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /app/
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
