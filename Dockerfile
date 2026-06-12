FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5005

CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:5005", "app:app"]
