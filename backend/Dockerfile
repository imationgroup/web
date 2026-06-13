FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Pillow needs libjpeg / libwebp / zlib headers in the build, plus a few
# bcrypt-related bits. Keep the layer small.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo libwebp7 libpng16-16 zlib1g \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
