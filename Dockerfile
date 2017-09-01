FROM python:3.6-alpine3.6
RUN mkdir -p /data ; mkdir -p /app
COPY requirements.txt /app
COPY deploy_time.py /app
RUN pip install -r /app/requirements.txt
CMD python /app/deploy_time.py
