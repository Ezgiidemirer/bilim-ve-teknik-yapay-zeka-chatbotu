# 🔹 Küçük, kararlı Python 3.10 imajı
FROM python:3.10-slim

# 🔹 Sistem bağımlılıkları (ChromaDB ve SentenceTransformers için)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# 🔹 Çalışma dizini
WORKDIR /app

# 🔹 Gereksinimleri kopyala ve yükle
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 🔹 Uygulama dosyalarını kopyala
COPY . .

# 🔹 Streamlit konfigürasyonu (Cloud Run için)
RUN mkdir -p ~/.streamlit && \
    echo "[server]\nport = 8080\nheadless = true\nenableCORS = false\nenableXsrfProtection = false\n" > ~/.streamlit/config.toml

# 🔹 Ortam değişkenleri
ENV PORT=8080
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_BROWSER_GATHERUSAGESTATS=false
ENV PIP_NO_CACHE_DIR=1
ENV OMP_NUM_THREADS=1
ENV TOKENIZERS_PARALLELISM=false

# 🔹 Cloud Run 8080 portunu dinler
EXPOSE 8080

# 🔹 Uygulamayı başlat (senin klasör yapına uygun)
CMD ["streamlit", "run", "rag_yapayzeka_chatbot/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
