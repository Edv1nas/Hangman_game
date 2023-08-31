FROM python:3.9

WORKDIR /frontend
COPY application/frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY application/frontend/. /frontend
EXPOSE 1455
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "1455"]