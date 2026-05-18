FROM python:3.11.14

COPY * /

RUN pip install -r req.txt

CMD ["python", "botcore.py"]