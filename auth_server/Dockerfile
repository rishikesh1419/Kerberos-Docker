FROM python:3
WORKDIR /usr/src/app
COPY auth_server.py ./
COPY pub_as_tgs.pem ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","auth_server.py"]
