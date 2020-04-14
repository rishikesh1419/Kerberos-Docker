FROM python:3
WORKDIR /usr/src/app
COPY ticket_grant_server.py ./
COPY pub_tgs_server.pem ./
COPY pri_as_tgs.pem ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","ticket_grant_server.py"]
