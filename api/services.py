import json
import requests

from .config import API_ADV_TOKEN


def get_api_advisor_data(city_id):
    """
    Make a request to API Advisor and 
    return data and status code
    """
    url = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{0}/days/15?token={1}'.format(
        city_id,
        API_ADV_TOKEN
    )

    response = requests.get(url)

    return response.json(), response.status_code