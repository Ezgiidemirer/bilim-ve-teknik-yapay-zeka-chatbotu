# Temel Python imajı
FROM python:3.10-slim

# Çalışma dizini
WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı kopyala
COPY . .

# Streamlit portunu ayarla
EXPOSE 8080

# Streamlit ayarları
ENV PORT 8080
ENV STREAMLIT_SERVER_PORT 8080
ENV STREAMLIT_SERVER_HEADLESS true
ENV STREAMLIT_SERVER_ENABLECORS false

# Uygulamayı başlat
CMD ["streamlit", "run", "rag_yapayzeka_chatbot/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
