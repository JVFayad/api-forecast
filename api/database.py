from .models import db


def get_queryset(model):
    queryset = model.query.all()
    return queryset

def create_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_operations()

def commit_operations():
    db.session.commit()