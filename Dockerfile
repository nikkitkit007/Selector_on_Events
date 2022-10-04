FROM python:latest

WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
RUN chmod +x ./gunicorn.sh

#RUN python run_for_create_api.py

#ENTRYPOINT ["./gunicorn.sh && python /usr/src/app/server/event_controller.py"]
#CMD [ "python", "./data_base/__main__.py"]
#RUN ["python data_base/__main__.py"]
#ENTRYPOINT ["./gunicorn.sh"]
