FROM python:3.11.9-bookworm

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p ${DAGSTER_HOME}
COPY . ${DAGSTER_HOME}
WORKDIR ${DAGSTER_HOME}

RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt update
RUN ACCEPT_EULA=Y apt install -y msodbcsql18
RUN ACCEPT_EULA=Y apt install -y unixodbc
RUN apt install -y unixodbc-dev

RUN pip install -e ".[dev]"

EXPOSE 4000
