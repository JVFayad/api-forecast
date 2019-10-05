import json
import requests

from datetime import datetime

from flask import request

from . import create_app
from .models import Forecast, db
from .config import API_ADV_TOKEN
from .database import create_update_instance, get_queryset

from sqlalchemy import desc, func
from sqlalchemy.sql import label

app = create_app()


@app.route('/cidade', methods=['GET'])
def update_forecast_database():
    city_id = request.args.get('id')

    if not city_id:
        return json.dumps(
            {
                'error': True, 
                'detail': 'Missing parameter city Id (?id=<ID>)'
            }
        ), 400
    
    url = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{0}/days/15?token={1}'.format(
        city_id,
        API_ADV_TOKEN
    )

    response = requests.get(url)
    response_json = response.json()

    if response.status_code != 200:
        return json.dumps(response_json), response.status_code

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

@app.route('/analise', methods=['GET'])
def get_forecast_analysis():
    initial_date = request.args.get('data_inicial')
    final_date = request.args.get('data_final')

    if not initial_date or not final_date:
        return json.dumps(
            {
                'error': True, 
                'detail': 'Missing parameters (?data_inicial=<DATA_INICIAL>&data_final=<DATA_FINAL>)'
            }
        ), 400

    initial_date = datetime.strptime(
        initial_date, '%Y-%m-%d').date()

    final_date = datetime.strptime(
        final_date, '%Y-%m-%d').date()

    queryset = Forecast.query.filter(
            func.DATE(Forecast.date) >= initial_date
        ).filter(
            func.DATE(Forecast.date) <= final_date)

    city_max_temp = queryset.order_by(desc(Forecast.max_temp)).first()

    city_prect_avg = db.session.query(
        Forecast, label(
            'rain_prect_avg', func.avg(Forecast.rain_prect)
        )).filter(
            func.DATE(Forecast.date) >= initial_date
        ).filter(
            func.DATE(Forecast.date) <= final_date
        ).group_by(Forecast.city).all()    

    response = json.dumps({
        'max_temperature': {
            'city': city_max_temp.city,
            'temperature': city_max_temp.max_temp
        },
        'preciptation_average': [{
            'city': city_avg[0].city, 
            'average': round(city_avg[1], 1)
        } for city_avg in city_prect_avg],       
    }, ensure_ascii=False)

    return response
