FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get -y install unixodbc unixodbc-dev
RUN apt-get -y install curl gnupg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/microsoft.list
RUN echo "deb [arch=amd64,arm64,armhf] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/microsoft.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "startup.py"]