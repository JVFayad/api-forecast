import json

from datetime import datetime

from flask import request

from . import create_app
from .database import create_update_forecast, max_temperature_inrange, preciptation_average_inrange
from .services import get_api_advisor_data


app = create_app()


@app.route('/cidade', methods=['GET'])
def update_forecast_database():
    """
    Save the Forecast information retrieved 
    from API Advisor on database
    """
    city_id = request.args.get('id')

    if not city_id:
        return json.dumps(
            {
                'error': True, 
                'detail': 'Missing parameter city Id (?id=<ID>)'
            }
        ), 400
    
    request_data, status_code = get_api_advisor_data(city_id)

    if status_code != 200:
        return json.dumps(request_data), status_code

    city = request_data['name']
    state = request_data['state']
    country = request_data['country'] 

    for forect in request_data['data']:
        create_update_forecast(
            city=city,
            state=state,
            country=country,
            date=datetime.strptime(
                forect['date'], "%Y-%m-%d").date(),
            rain_probab=forect['rain']['probability'],
            rain_prect=forect['rain']['precipitation'],
            max_temp=forect['temperature']['max'],
            min_temp=forect['temperature']['min'],
        )

    response = json.dumps({'message': 'Forecast data updated'})
    return response, 200


@app.route('/analise', methods=['GET'])
def get_forecast_analysis():
    """
    Get Forecast Analyisis with max temperature 
    and rain precipitation average
    """
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

    city_max, temp_max =  max_temperature_inrange(
        initial_date, final_date)

    city_prect_avg = preciptation_average_inrange(
        initial_date, final_date
    )  

    response = json.dumps({
        'max_temperature': {
            'city': city_max,
            'temperature': temp_max
        },
        'preciptation_average': [{
            'city': city_avg[0].city, 
            'average': round(city_avg[1], 1)
        } for city_avg in city_prect_avg],       
    }, ensure_ascii=False)

    return response, 200
