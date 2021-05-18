FROM pypy:latest

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get -y update
RUN apt-get -y install memcached
RUN pypy3 -m pip install --upgrade pip
RUN pypy3 -m pip install --no-cache-dir -r requirements.txt

COPY . .
ADD start.sh /
RUN chmod +x /start.sh

EXPOSE 7001

ENV PYTHONHASHSEED 0

CMD ["/start.sh"]
