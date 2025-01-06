FROM python:3.11-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
RUN uv sync

COPY ./site /code/

CMD ["fastapi", "run", "main.py", "--port", "8000"]
