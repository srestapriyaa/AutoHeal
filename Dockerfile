
FROM python:3.14-slim

WORKDIR /app

COPY app.py .
COPY monitor.py .

CMD ["python", "monitor.py"]
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"