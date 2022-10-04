FROM python:3.8.1-slim-buster

ENV WORKDIR=/app
ENV USER=app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR $WORKDIR

RUN pip install --upgrade pip
COPY ./requirements.txt $WORKDIR/requirements.txt
RUN pip install -r requirements.txt

RUN adduser --system --group $USER

COPY . $WORKDIR
RUN chown -R $USER:$USER $WORKDIR
USER $USER