FROM python:3.11
WORKDIR /app
RUN apt-get update && apt-get install -y && apt-get clean
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .