FROM python:latest

WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
RUN chmod +x ./gunicorn.sh

#ENTRYPOINT ["./gunicorn.sh && python /usr/src/app/server/event_controller.py"]
#CMD [ "python", "./data_base/__main__.py"]
#RUN ["python data_base/__main__.py"]
#ENTRYPOINT ["./gunicorn.sh"]
