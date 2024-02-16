# pull base image
FROM python:3.10.9
# set workdir
WORKDIR  /app

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . /app