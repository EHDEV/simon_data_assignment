FROM python:3.8

WORKDIR /tmp

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /code

COPY . /code

COPY dataset/ .

# command to run on container start
CMD [ "python", "./data_loader.py" ]