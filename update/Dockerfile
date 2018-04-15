FROM python:3.6.5-alpine3.7

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD . /app

CMD [ "python", "update.py" ]
