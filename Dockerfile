FROM python:3
WORKDIR /src/app/
COPY project/requirements.txt /src/app/
# RUN apt-get update && apt-get upgrade -y && apt-get install -y apt-utils python3-dev python3-pip
RUN pip3 install -r requirements.txt
