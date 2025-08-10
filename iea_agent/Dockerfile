FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl bash git build-essential libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libasound2 libxshmfence1 libx11-xcb1 libxext6 libx11-6 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 🟢 Copy sources BEFORE installing (so Hatch can see them)
COPY pyproject.toml /app/
COPY src /app/src
COPY tests /app/tests

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir .

RUN python -m playwright install --with-deps

ENV PYTHONUNBUFFERED=1

