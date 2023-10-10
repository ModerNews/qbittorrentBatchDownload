FROM python:3.11-alpine
LABEL author="Grzegorz Jagielski"

COPY app/qbitWrapper /app/qbitWrapper
COPY app/requirements.txt /tmp/requirements.txt
COPY app/*.py /app/

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk del .build-deps gcc musl-dev

WORKDIR /app

CMD ["python", "main.py"]