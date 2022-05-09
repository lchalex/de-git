FROM python:3.8
COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt