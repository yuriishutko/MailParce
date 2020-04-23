FROM python
RUN apt-get -y update && apt-get -y install python3 gcc python3-dev python3-pip
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip3 install -r ./pip-requirements.txt
CMD python3 telegram_bot.py