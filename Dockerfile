FROM python:3.11.4-slim-bullseye

WORKDIR /app

RUN pip install --no-cache-dir Flask
RUN pip install --no-cache-dir flask_sqlalchemy
RUN pip install --no-cache-dir flask-marshmallow
RUN pip install --no-cache-dir requests

CMD [ "python3", "main.py"]