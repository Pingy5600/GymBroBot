FROM python:3.8.2

WORKDIR /.

COPY . .

RUN pip install -r requirements.txt