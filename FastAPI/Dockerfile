FROM python:3.8

COPY . .

RUN pip install -r requirements.txt
RUN pip install scikit-learn==1.2.2

EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port 8000
