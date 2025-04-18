FROM python:3.10-slim AS builder

WORKDIR /app
ENV IN_DOCKER=true

COPY docs/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY docs/docs /app/docs

COPY src /app/src

ENV PYTHONPATH=/app/docs

RUN sphinx-build -b html /app/docs /app/syntax_folder

FROM nginx:alpine

COPY --from=builder /app/syntax_folder /usr/share/nginx/html

COPY docs/nginx/default.conf /etc/nginx/templates/default.conf.template
