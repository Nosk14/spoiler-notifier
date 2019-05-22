FROM python:3.7.2-slim-stretch
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY spoiler-notifier /usr/local/spoiler-notifier/
WORKDIR /usr/local/spoiler-notifier/src
CMD python main.py