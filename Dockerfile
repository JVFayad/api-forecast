FROM python:3
ENV PYTHONUNBUFFERED 1
RUN pip install pipenv
COPY . /code
WORKDIR /code/api
RUN pipenv install --system --deploy
ENV FLASK_APP /code/api/app.py
CMD ["flask", "run", "--host", "0.0.0.0"]