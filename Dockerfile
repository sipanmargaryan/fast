FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TF_ENABLE_ONEDNN_OPTS 3

WORKDIR /app

USER root

COPY requirements.txt pyproject.toml poetry.lock ./

RUN pip3 --no-cache-dir install -r requirements.txt
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ADD . /app/

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "3"]
