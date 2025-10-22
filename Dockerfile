# 🔹 Temel Python imajı (küçük boyutlu ve hızlı)
FROM python:3.10-slim

# 🔹 Sistem bağımlılıklarını yükle (Chromadb ve SentenceTransformers için)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 🔹 Çalışma dizini oluştur
WORKDIR /app

# 🔹 Gereksinimleri kopyala ve pip'i güncelle
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 🔹 Uygulama dosyalarını kopyala
COPY . .

# 🔹 Streamlit port ayarı
EXPOSE 8080

# 🔹 Streamlit ortam değişkenleri
ENV PORT=8080
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_BROWSER_GATHERUSAGESTATS=false
ENV PIP_NO_CACHE_DIR=1

# 🔹 Bellek optimizasyonu
ENV OMP_NUM_THREADS=1
ENV TOKENIZERS_PARALLELISM=false

# 🔹 Uygulamayı başlat
CMD ["streamlit", "run", "rag_yapayzeka_chatbot/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
