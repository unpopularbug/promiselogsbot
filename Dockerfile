FROM python:3.12.4

RUN apt-get update \
    && apt-get -y install binutils libproj-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir wheel \
    && mkdir /app

WORKDIR /app

COPY . /app/

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
