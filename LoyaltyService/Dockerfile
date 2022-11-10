FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app/LoyaltyService

COPY requirements.txt /app/LoyaltyService/requirements.txt

RUN pip install -r requirements.txt

COPY . /app/LoyaltyService

#CMD ["python3", "LoyaltyService/manage.py","runserver", "0.0.0.0:8050"]
