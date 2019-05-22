FROM python:3.7.2-slim-stretch
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src /usr/local/src
WORKDIR /usr/local/src
CMD python main.py