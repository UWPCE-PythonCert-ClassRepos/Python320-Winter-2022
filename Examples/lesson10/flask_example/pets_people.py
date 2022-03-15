"""
really simple Flask app to demonstrate testing

to run it:

Linux or Mac:

export FLASK_APP=pets_people
flask run

Windows CMD:

> set FLASK_APP=pets_people
> flask run

Windows Powershell:

> $env:FLASK_APP="pets_people"
> flask run

"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    """
    root page: html help.
    """
    return """<h1>Pets and People</h1>
    <p>Simple API For info about pets and people</p>
    <h2>Endpoints:</h2>
    <pre>
    /pets: returns a list of pet info

    /people: returns a list of people info
    </pre>
    """

PETS_DATA = [{"name": "Sesame",
              "species": "cat",
              "breed": "Persian"},
             {"name": "Sassy",
              "species": "dog",
              "breed": "Daschund"},
              ]

PEOPLE_DATA = [{"first_name": "Chris",
                "last_name": "Barker",
                "pets": ["Sesame", "Sassy"],
                },
                {"first_name": "Nancy",
                "last_name": "Jones",
                "pets": ["Wilma", "Etta"],
                },
                ]
