FROM python:3.9

WORKDIR /app
COPY application/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY application/backend/. /app
EXPOSE 1456

CMD python -m unittest -v; python main.py 