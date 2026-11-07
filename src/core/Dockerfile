FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "--threads", "8", "-b", "0.0.0.0:8080", "app:app"]
