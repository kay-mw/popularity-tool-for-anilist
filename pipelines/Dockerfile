FROM python:3.10-slim

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

RUN mkdir -p ${DAGSTER_HOME}

COPY . ${DAGSTER_HOME}

WORKDIR ${DAGSTER_HOME}

RUN pip install -e ".[dev]"

EXPOSE 3000
