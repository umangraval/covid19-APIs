FROM ubuntu:18
RUN apt-get update -y 
RUN apt-get install python-pip gunicorn3 -y
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "app:app", "--workers=5"]