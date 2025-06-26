FROM python:3.10-slim AS builder

WORKDIR /app
ENV IN_DOCKER=true \
    PYTHONPATH=/app/docs:$PYTHONPATH

COPY docs/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY docs/docs /app/docs

COPY src /app/src

RUN sphinx-build -a -E -b html /app/docs /app/syntax_folder

FROM public.ecr.aws/rogii/nginx:mainline

COPY --from=builder /app/syntax_folder /usr/share/nginx/html

COPY docs/nginx/default.conf /etc/nginx/conf.d/default.conf
