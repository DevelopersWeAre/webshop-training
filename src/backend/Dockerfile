FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update && apt upgrade -fy

RUN mkdir /webshop
ADD requirements.txt /webshop

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /webshop/requirements.txt

COPY ./webshop/ /webshop/
ADD ./webshop/ /webshop/
WORKDIR /webshop/

EXPOSE 8000
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
# #RUN python manage.py runserver 127.0.0.1:8000
RUN python manage.py runserver --settings=webshop.settings.dev 127.0.0.1:8000
RUN echo $PWD

