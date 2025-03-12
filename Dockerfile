FROM python:3.12.9-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    portaudio19-dev \
    pulseaudio \
    ffmpeg \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# For google auth
RUN pip install --no-cache-dir google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client  

CMD ["python", "src/app.py"]
