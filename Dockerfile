FROM python:3.10

RUN mkdir /bot

WORKDIR /bot

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY wildberries-notification-bot_aiogram3 .

RUN chmod a+x docker/*.sh

#CMD ["poetry", "run", "python", "bot.py"]