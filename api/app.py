import json

from flask import request

from . import create_app
from .models import Forecast, db


app = create_app()


@app.route('/', methods=['GET'])
def get_all():
    teste = {
        "teste": "testei"
    }

    return json.dumps(teste), 200