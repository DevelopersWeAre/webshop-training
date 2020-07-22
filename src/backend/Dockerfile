FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update && apt upgrade -fy

RUN mkdir /webshop
ADD requirements.txt /webshop

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /webshop/requirements.txt

COPY . /webshop
ADD . /webshop
WORKDIR /webshop/

EXPOSE 8000

