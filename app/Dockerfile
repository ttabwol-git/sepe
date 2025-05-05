# Build stage
FROM python:3.13.3-slim AS builder
WORKDIR /app
COPY . .

# Runtime stage
FROM python:3.13.3-slim
WORKDIR /app
COPY --from=builder /app/pyproject.toml /app/poetry.lock* ./
RUN pip install poetry==2.1.2
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY --from=builder /app .
EXPOSE 8000
CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000", "--log-level", "critical"]