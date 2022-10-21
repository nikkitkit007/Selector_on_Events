FROM python:latest

WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
RUN chmod +x ./gunicorn.sh

