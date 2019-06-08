FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install python-telegram-bot==12.0.0b1 --upgrade
CMD python ./main.py