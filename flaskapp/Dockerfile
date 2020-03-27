FROM ubuntu
RUN apt-get update -y 
RUN apt-get install python-pip -y
RUN apt install -y libsm6
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py","&","python","app.py"]
