FROM python:3.12.7-slim
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /opt/
WORKDIR /opt
EXPOSE 8001
ENTRYPOINT  uvicorn main:app --host=0.0.0.0 --port=8001
