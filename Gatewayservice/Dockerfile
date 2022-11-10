FROM python:3.9


ENV PYTHONUNBUFFERED 1

WORKDIR /app/Gatewayservice

COPY requirements.txt /app/Gatewayservice/requirements.txt

RUN pip install -r requirements.txt

COPY . /app/Gatewayservice

#CMD ["python3", "Gatewayservice/manage.py","runserver", "0.0.0.0:8080"]
