FROM python:3.9.1

# FROM alpine:3.7
# EXPOSE 3031
# VOLUME /usr/src/app/public
# WORKDIR /usr/src/app
# RUN apk add --no-cache uwsgi-python3 python3
# COPY . .
# RUN rf -rf public/*
# RUN pip3 install --no-cache-dir -r requirements.txt
# CMD [ "uwsgi", "--socket", "0.0.0.0:3031", "--uid", "uwsgi", "--plugins", "python3", "--protocol", "uwsgi", "--wsgi", "main:application" ]

ADD . /app
WORKDIR /app
RUN pip install -r requiments.txt
CMD ["server.py"]
