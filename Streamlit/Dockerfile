FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip3 install -r requirements.txt
RUN pip install protobuf==3.20.0
RUN pip install altair==4.1.0  

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]
