FROM python:3.11-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD fastapi run ./refactor_app/main.py
