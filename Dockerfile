FROM python:3.8-slim

COPY ./app /app
COPY requirements.txt .
RUN apt-get update \	
    && apt-get install gcc -y \	
    && apt-get clean
RUN pip --no-cache-dir install -r requirements.txt