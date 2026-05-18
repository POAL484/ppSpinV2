FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && python -m venv /opt/venv/ && /opt/venv/bin/pip install --upgrade pip setuptools wheel

RUN /opt/venv/bin/pip install -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /opt/venv/ /opt/venv/
COPY * ./

CMD ["/opt/venv/bin/python", "./botcore.py"]