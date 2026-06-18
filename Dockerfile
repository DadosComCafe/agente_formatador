FROM python:3.14-slim-trixie

WORKDIR /app

COPY convert_types.py convert_types.py
COPY utils utils

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    openpyxl \
    google-genai

EXPOSE 8501

CMD ["streamlit", "run", "convert_types.py", "--server.address=0.0.0.0", "--server.enableCORS=false"]