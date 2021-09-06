FROM python:3

ADD roborock-exporter.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./roborock-exporter.py" ]