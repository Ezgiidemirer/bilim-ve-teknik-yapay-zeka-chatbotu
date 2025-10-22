# 1_prepare_data.py
# LangChain 0.2+ uyumlu: PDF -> Temizleme -> Chunk -> JSON

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import re

# === Dosya yolları ===
pdf_path = "yazi.pdf"
output_json = "yapay_zeka_chunks_clean2.json"

# === Yardımcı temizleme fonksiyonu ===
def clean_text(text):
    # PDF sayfa altlıklarını, satır sonlarını ve gereksiz boşlukları temizle
    text = re.sub(r"\d{2}_\d{2}_.*?indd.*?\d{2}:\d{2}", " ", text)  # sayfa dip notu
    text = re.sub(r"-\n", "", text)  # tireyle bölünen kelimeleri birleştir
    text = re.sub(r"\n+", "\n", text)  # fazla boş satırları azalt
    text = re.sub(r"\s+", " ", text)  # fazla boşlukları düzelt

    # Şapkalı a’yı düzelt
    text = text.replace("â", "a")

    return text.strip()

# === PDF yükleme ===
print("📘 PDF yükleniyor...")
loader = PyPDFLoader(pdf_path)
documents = loader.load()
print(f"📄 {len(documents)} sayfa bulundu.")

# === Temizleme ===
for doc in documents:
    doc.page_content = clean_text(doc.page_content)

# === Chunk (parça) oluşturma ===
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,        # daha uzun parça
    chunk_overlap=200,     # bağlam koruma
    separators=["\n\n", "\n", ". ", " "]  # anlamlı bölmeler
)

texts = text_splitter.split_documents(documents)

# === Kısa chunk’ları filtrele ===
filtered_texts = [
    doc for doc in texts if len(doc.page_content.strip())>120
]
# === JSON’a kaydetme ===
data = [
    {"page": doc.metadata.get("page", 0), "content": doc.page_content}
    for doc in filtered_texts
]

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ {len(data)} temiz metin parçası oluşturuldu ve '{output_json}' dosyasına kaydedildi.")
