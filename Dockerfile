FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel

RUN /opt/venv/bin/pip install -r requirements.txt


FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY commands_spin/ ./commands_spin/
COPY events_spin/ ./events_spin/
COPY types_spin/ ./types_spin/

COPY botconfig.py .
COPY botcore.py .
COPY .env .
COPY fetch_emotes.py .
COPY momsjokes.py .
COPY mongo.py .
COPY utils.py .

ENV PYTHONPATH=/app

CMD ["/opt/venv/bin/python", "botcore.py"]