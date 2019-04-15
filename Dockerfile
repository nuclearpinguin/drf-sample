FROM python:3.7

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .
