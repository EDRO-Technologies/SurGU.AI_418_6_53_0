FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

FROM base AS deps

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-cache --python 3.13 --only-dev

FROM deps AS src

COPY src ./src

FROM base AS final

COPY --from=deps /code/.venv /code/.venv
COPY --from=src /code/src /code/src

ENV PATH="/code/.venv/bin:$PATH" \
    PYTHONPATH="/code/src" \
    TRANSFORMERS_CACHE=/root/.cache/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/root/.cache/huggingface

WORKDIR /code

EXPOSE 8080
