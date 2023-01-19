# 
FROM python:3.11

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./model_server /app/model_server

# 
CMD ["uvicorn", "model_server.main:app", "--host", "0.0.0.0", "--port", "80"]
