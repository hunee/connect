FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app/
ENV DOCKER True
ENV PYTHONUNBUFFERED 0
#ENV FLASK_APP hello.py
#CMD flask run --host=0.0.0.0
#RUN chmod +x server.sh
#CMD server.sh 0.0.0.0 5000
#cmd python3 -m app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--log-config", "./logging.yaml", "--reload"]
