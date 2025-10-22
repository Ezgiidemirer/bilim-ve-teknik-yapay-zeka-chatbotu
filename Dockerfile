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

# pip'i güncelle ve bağımlılıkları kur
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 🔹 Uygulama dosyalarını kopyala
COPY . .

# 🔹 Streamlit ortam değişkenleri (Cloud Run uyumlu)
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

# 🔹 Çalıştırılacak komut
CMD ["streamlit", "run", "rag_yapayzeka_chatbot/app.py", "--]()
