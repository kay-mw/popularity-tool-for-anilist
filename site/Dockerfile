FROM python:3.11-slim-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

RUN --mount=type=secret,id=STORAGE_CONNECTION_STRING,env=STORAGE_CONNECTION_STRING

CMD ["fastapi", "run", "main.py", "--port", "8000"]
