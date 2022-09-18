FROM python:latest

WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
RUN chmod +x ./gunicorn.sh
CMD ["python", "server/event_controller.py"]

#ENTRYPOINT ["./gunicorn.sh && python /usr/src/app/server/event_controller.py"]
