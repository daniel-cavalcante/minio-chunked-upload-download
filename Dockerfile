FROM python:3.8-slim-buster

WORKDIR /home/app

# RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

# CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]

ENTRYPOINT ["sh", "./entrypoint.sh"]
