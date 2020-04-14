FROM python:3
WORKDIR /usr/src/app
COPY server.py ./
COPY requirements.txt ./
COPY pri_tgs_server.pem ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","server.py"]
