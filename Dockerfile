# Etapa base: lo común a todo
FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

# Etapa de tests: agrega dependencias de desarrollo
FROM base AS test

RUN uv sync --locked --no-install-project
COPY . .
RUN uv sync --locked

CMD ["pytest"]

# Etapa final: la imagen de la API
FROM base AS runtime

COPY . .
RUN uv sync --locked --no-dev

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]