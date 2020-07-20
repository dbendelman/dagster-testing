FROM python:3.7.7
ARG VARIANT

RUN apt-get update -qq
RUN apt-get install -qqy libpq-dev

WORKDIR /src
ENV PYTHONPATH /src

COPY requirements-${VARIANT}.txt .
RUN set -ex; \
    pip install --no-cache-dir -r requirements-${VARIANT}.txt; \
    rm -rf /root/.cache

COPY . .
RUN pip install --no-cache-dir .
