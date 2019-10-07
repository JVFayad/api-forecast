from .models import db, Forecast

from sqlalchemy import desc, func
from sqlalchemy.sql import label


def create_instance(model, **kwargs):
    """
    Create instance for 
    choosen model
    """
    instance = model(**kwargs)
    db.session.add(instance)
    commit_operations()


def update_instance(instance, **kwargs):
    """
    Update choosen instance
    """
    for attr in kwargs.keys():
        setattr(instance, attr, kwargs[attr])

    commit_operations()


def create_update_forecast(**kwargs):
    """
    Create/Update Forecast data
    """
    model = Forecast

    # If forecast with city, state and date passed
    # already exists, info is updated
    instance = model.query.filter(
            model.city == kwargs.get('city')
        ).filter(
            model.state == kwargs.get('state')
        ).filter(
            func.DATE(model.date) == kwargs.get('date')
        ).first()

    if instance:
        update_instance(instance, **kwargs)
    else:
        create_instance(model, **kwargs)


def max_temperature_inrange(initial_date, final_date):
    """
    Get city with max temperature
    and the temperature itself
    """
    model = Forecast

    city_max_temp = model.query.filter(
            func.DATE(model.date) >= initial_date
        ).filter(
            func.DATE(model.date) <= final_date
        ).order_by(desc(model.max_temp)).first()

    if not city_max_temp:
        return None, 0
    
    return city_max_temp.city, city_max_temp.max_temp


def preciptation_average_inrange(initial_date, final_date):
    """
    Get rain precipitation average by city
    """
    model = Forecast
    
    city_prect_avg = db.session.query(
        model, label(
            'rain_prect_avg', func.avg(model.rain_prect)
        )).filter(
            func.DATE(model.date) >= initial_date
        ).filter(
            func.DATE(model.date) <= final_date
        ).group_by(model.city).all()  

    return city_prect_avg


def commit_operations():
    """
    Commit database changes
    """
    db.session.commit()