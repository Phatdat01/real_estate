FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

# Run the application
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "5000"]