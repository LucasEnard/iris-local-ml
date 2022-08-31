from turtle import back
from flask import Flask, jsonify, request, render_template

# from grongier.pex import Director
# from datetime import datetime

# from msg import (GetAllPersonRequest,CreatePersonRequest,
#                 UpdatePersonRequest,GetPersonRequest)
# from obj import Person

import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

app = Flask(__name__)

# GET Infos
@app.route("/", methods=["GET"])
def get_main():
    text_sentiment = open("src/app/static/alice29.txt").read()

    background_image = np.array(Image.open('src/app/static/recycleicon.jpg'))
    img_colors = ImageColorGenerator(background_image)
    wc = WordCloud(background_color = 'white', mask = background_image)
    wc.generate(text_sentiment)
    wc.recolor(color_func = img_colors)
    wc.to_file('src/app/static/wc.jpg')
    return render_template("main.html", cloud_image = "static/wc.jpg")

@app.route("/persons/", methods=["GET"])
def get_all_persons():
    """
    > The function creates a message object, creates a service object, and then dispatches the message
    to the service
    :return: A list of all the persons in the database.
    """
    msg = GetAllPersonRequest()
    service = Director.create_business_service("Python.FlaskService")
    response = service.dispatchProcessInput(msg)
    return jsonify(response.persons)

@app.route("/persons/", methods=["POST"])
def post_person():
    """
    > The function creates a new person object from the request body, creates a message object from the
    person object, and then dispatches the message to the business service
    :return: The response is being returned as a json object.
    """

    person = Person(**request.get_json())
    
    msg = CreatePersonRequest(person=person)

    service = Director.create_business_service("Python.FlaskService")
    response = service.dispatchProcessInput(msg)

    return jsonify(response)

# GET person with id
@app.route("/persons/<int:id>", methods=["GET"])
def get_person(id):
    """
    > The function takes an id as a parameter, creates a message, creates a service, and dispatches the
    message to the service
    
    :param id: The id of the person to get
    :return: A JSON object
    """
    msg = GetPersonRequest(id)

    service = Director.create_business_service("Python.FlaskService")
    response = service.dispatchProcessInput(msg)
    return jsonify(response)

# PUT to update person with id
@app.route("/persons/<int:id>", methods=["PUT"])
def update_person(id:int):
    """
    > The function takes the id of the person to update, creates a new person object from the request
    body, creates a message object, sets the id of the message object, creates a service object, and
    dispatches the message to the service
    
    :param id: The id of the person to update
    :return: The response is being returned as a json object.
    """

    person = Person(**request.get_json())
    msg = UpdatePersonRequest(person=person)
    msg.id = id

    service = Director.create_business_service("Python.FlaskService")
    response = service.dispatchProcessInput(msg)

    return jsonify(response)

# DELETE person with id
@app.route("/persons/<int:id>", methods=["DELETE"])
def delete_person(id):
    """
    > The function takes an id as an argument, creates a DeletePersonRequest message, sets the id
    property of the message to the id argument, creates a business service, dispatches the message to
    the service, and returns the response
    
    :param id: The id of the person to delete
    :return: A JSON object with the response from the service.
    """
    msg = DeletePersonRequest(person=person)
    msg.id = id

    service = Director.create_business_service("Python.FlaskService")
    response = service.dispatchProcessInput(msg)

    return jsonify(response)


# ----------------------------------------------------------------
### MAIN PROGRAM
# ----------------------------------------------------------------

if __name__ == '__main__':
    app.run('0.0.0.0', port = "8080")