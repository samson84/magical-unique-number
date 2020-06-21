FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENV STATIC_URL /game
