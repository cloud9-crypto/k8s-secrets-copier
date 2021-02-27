FROM python:3

WORKDIR /tmp
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "secretscopier.py"]