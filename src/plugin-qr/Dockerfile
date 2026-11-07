FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org Flask==3.1.1 gunicorn==23.0.0
COPY app.py .
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8081", "app:app"]
