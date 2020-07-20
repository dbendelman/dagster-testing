FROM python:3.7.7
ARG DAGSTER_VERSION

RUN apt-get update -qq
RUN apt-get install -qqy libpq-dev

WORKDIR /src
ENV PYTHONPATH /src

COPY requirements-${DAGSTER_VERSION}.txt .
RUN set -ex; \
    pip install --no-cache-dir -r requirements-${DAGSTER_VERSION}.txt; \
    rm -rf /root/.cache

COPY . .
RUN pip install --no-cache-dir .
