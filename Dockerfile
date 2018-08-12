FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
#RUN cat init.txt | redis-cli --pipe
CMD ["python", "app.py"]