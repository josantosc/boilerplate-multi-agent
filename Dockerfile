# Etapa de construção
FROM python:3.10.13-slim as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc libcurl4-openssl-dev libssl-dev \
    && apt-get clean


COPY requirements.txt .
RUN pip install --upgrade pip setuptools


RUN pip install --no-cache-dir -r requirements.txt

# Etapa de produção
FROM python:3.10.13-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder / /

COPY . .

# Copiar e configurar o arquivo start.sh
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]