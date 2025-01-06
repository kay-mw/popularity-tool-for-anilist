FROM python:3.11-slim-bookworm

WORKDIR /code

COPY ../pyproject.toml /code/pyproject.toml
RUN uv sync

COPY . /code/

CMD ["fastapi", "run", "main.py", "--port", "8000"]
