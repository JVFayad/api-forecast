from .models import db
from sqlalchemy import func


def get_queryset(model):
    queryset = model.query.all()
    return queryset

def create_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_operations()

def create_update_instance(model, **kwargs):
    instance = model.query.filter(
            model.city == kwargs.get('city')
        ).filter(
            func.DATE(model.date) == kwargs.get('date')
        ).first()

    if instance:
        for attr in kwargs.keys():
            setattr(instance, attr, kwargs[attr])
    else:
        instance = model(**kwargs)
        db.session.add(instance)

    commit_operations()

def commit_operations():
    db.session.commit()