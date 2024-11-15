FROM python:3

ADD . /opt/server
WORKDIR /opt/server
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]