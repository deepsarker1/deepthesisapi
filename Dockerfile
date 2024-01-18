from python:3.10.9
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_DEBUG 1

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3005
ENV PYTHONPATH /app

# CMD gunicorn app.wsgi:app -w 1 --bind 0.0.0.0:3005 --reload