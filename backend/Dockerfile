FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get -y update
RUN apt-get install -y python3 python3-pip python3-distutils netcat

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN chmod +x entrypoint.sh
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]
