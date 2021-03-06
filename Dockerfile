FROM python:3.8-alpine

WORKDIR /src

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY tracklist.txt .env ./
COPY bot/ ./

CMD ["python", "./main.py"]

