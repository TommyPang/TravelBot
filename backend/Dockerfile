FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Run app.py when the container launches
CMD exec gunicorn --bind=0.0.0.0 --timeout 600 app:app