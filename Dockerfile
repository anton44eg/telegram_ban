FROM python:3.10

RUN mkdir /app
WORKDIR /app
RUN python -m pip -q --no-cache-dir install poetry==1.1.12 && \
    python -m poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .
RUN python -m poetry install -q --no-interaction --no-dev && \
    python -m poetry cache clear --no-interaction pypi --all

COPY . .

COPY . /app
#ENV APP_ID $APP_ID
#ENV API_HASH $API_HASH
#ENTRYPOINT python main.py
