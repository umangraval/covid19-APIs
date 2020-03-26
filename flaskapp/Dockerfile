FROM ubuntu
RUN apt-get update -y 
RUN apt-get install python-pip -y
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py", "&&", "python", "bot.py"]
