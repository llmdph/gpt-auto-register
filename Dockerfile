FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OPENAI_SENTINEL_NODE_PATH=/usr/bin/node

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       ca-certificates curl bash nodejs \
  && rm -rf /var/lib/apt/lists/* \
  && node --version \
  && python --version

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Code is also bind-mounted at runtime for live edits.
COPY . /app

EXPOSE 8765
CMD ["python", "start_webui.py", "--host", "0.0.0.0", "--port", "8765", "--no-browser"]
