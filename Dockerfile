FROM python:3
WORKDIR /usr/src/app

RUN pip install redis

COPY . .
CMD ["python", "redis_py.py"]
