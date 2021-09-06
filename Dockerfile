FROM python:3

LABEL description="Prometheus Exporter for roborock vacuums."

ADD roborock-exporter.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

ENV IP_ADDRESS=
ENV TOKEN=

CMD [ "python", "./roborock-exporter.py" ]