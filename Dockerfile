# the base image
FROM python:3.13.7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "retrieval_pipeline:app", "--host", "0.0.0.0"] # host 0.0.0.0 so this port is reachable from outside.

