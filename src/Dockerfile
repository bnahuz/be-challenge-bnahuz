FROM python:3.10.12
WORKDIR /src
RUN pip install --upgrade pip
RUN pip install flask pymongo requests
COPY . /src
ENV FLASK_APP=app
CMD ["python","app.py"]