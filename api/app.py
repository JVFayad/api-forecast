import json
import requests

from datetime import datetime

from flask import request

from . import create_app
from .models import Forecast, db
from .config import API_ADV_TOKEN
from .database import create_instance, create_update_instance


app = create_app()


@app.route('/cidade', methods=['GET'])
def get_all():
    city_id =  request.args.get('id')
    
    url = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{0}/days/15?token={1}'.format(
        city_id,
        API_ADV_TOKEN
    )

    response = requests.get(url)

    if response.status_code != 200:
        return json.dumps({'error': 'error'}), response.status_code

    response_json = response.json()

    city = response_json['name']
    state = response_json['state']
    country = response_json['country'] 

    for forect in response_json['data']:
        create_update_instance(
            Forecast,
            city=city,
            state=state,
            country=country,
            date=datetime.strptime(forect['date'], "%Y-%m-%d").date(),
            rain_probab=forect['rain']['probability'],
            rain_prect=forect['rain']['precipitation'],
            max_temp=forect['temperature']['max'],
            min_temp=forect['temperature']['min'],
        )

    return json.dumps({'message': 'Forecast data updated'}), 200