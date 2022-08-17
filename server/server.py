import sys
# import requests
# import data.bd_worker as bd
from flask import Flask, request


app = Flask(__name__)
sys.path.append('../')


@app.route('/')
def index():
    return "User info..."


@app.route('/api/add_event', methods=["POST"])
def add_event():                            # add event in db
    """
    :return:
    """
    # name, time_start, time_end,image,pdf, cost = request.values['event_name'], request.values[]
    name = request.json["name"]
    return name[::-1]
    # bd.add_event()
    # if not request.values['token'] in accepting_tokens:
    #     return "Access denied"


@app.route('/api/update_event', methods=["POST"])
def update_event():
    """
    :return:
    """
    # name, time_start, time_end,image,pdf, cost = request.values['event_name'], request.values[]
    name = request.json["name"]
    return name[::]


@app.route('/api/add_user', methods=["POST"])
def update_event():
    if request.method == "POST":

        pass
    else:
        pass
    name = request.json["name"]
    return name[::]


if __name__ == '__main__':
    app.run(debug=True)         # to see mistakes
