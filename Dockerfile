FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pygbag

COPY . .

EXPOSE 8000

CMD ["pygbag", "--bind", "0.0.0.0", "--port", "8000", "."]
