FROM mdowds/uwsgi:python3.6.5

RUN pip install virtualenv

WORKDIR /app
RUN virtualenv venv

ADD ./requirements.txt /app/requirements.txt
RUN source venv/bin/activate && pip install -r requirements.txt

ADD . /app

EXPOSE 4000

CMD [ "uwsgi", "--http-socket", "0.0.0.0:4000", \
                "--uid", "uwsgi", \
                "--manage-script-name", \
                "--plugins", "python3", \
                "--virtualenv",  "/app/venv", \
                "--mount", "/=api:app", \
                "--master"]
