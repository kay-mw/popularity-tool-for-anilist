FROM python:3.11-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt update
RUN ACCEPT_EULA=Y apt install -y msodbcsql18
RUN ACCEPT_EULA=Y apt install -y unixodbc
RUN apt install -y unixodbc-dev

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
RUN uv sync

COPY ./site /code/

CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "8000"]
