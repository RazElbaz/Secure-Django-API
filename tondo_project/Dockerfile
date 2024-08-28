FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir django djangorestframework
RUN pip install faker
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#docker build -t mydjangoapp .
#docker run -d -p 8000:8000 mydjangoapp
#docker logs --follow competent_khayyam