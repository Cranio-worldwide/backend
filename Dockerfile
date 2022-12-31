FROM python:3.9
WORKDIR /app
COPY . .
RUN pip3 install -r /app/requirements.txt --no-cache-dir