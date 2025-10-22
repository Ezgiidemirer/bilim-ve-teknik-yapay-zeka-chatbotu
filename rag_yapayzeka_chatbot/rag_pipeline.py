# rag_pipeline.py

import os
import json
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import google.generativeai as genai

# --- .env dosyasını yükle ---
load_dotenv()

# --- Google API anahtarı ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY .env dosyasında bulunamadı!")
os.environ["GOOGLE_API_KEY"] = api_key

# --- 1. Veri Yükleme ---
# JSON dosyasını bulunduğu klasörden dinamik olarak bulur
json_path = os.path.join(os.path.dirname(__file__), "yapay_zeka_chunks_clean2.json")
if not os.path.exists(json_path):
    raise FileNotFoundError(f"❌ Veri dosyası bulunamadı: {json_path}")

with open(json_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

docs = [
    Document(page_content=c["content"], metadata={"page": c.get("page", None)})
    for c in chunks
]

# --- 2. Embedding ve Vektör Veritabanı ---
embedding = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

# Eğer veritabanı mevcutsa yeniden embedding yapma
db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
if not os.path.exists(db_path):
    print("🔍 Yeni embedding veritabanı oluşturuluyor...")
    vectorstore = Chroma.from_documents(docs, embedding, persist_directory=db_path)
    vectorstore.persist()
else:
    print("📁 Var olan embedding veritabanı yükleniyor...")
    vectorstore = Chroma(persist_directory=db_path, embedding_function=embedding)

retriever = vectorstore.as_retriever(search_kwargs={"k": 15})

# --- 3. LLM (Gemini 2.5 Pro) ---
llm = GoogleGenerativeAI(model="gemini-2.5-pro")

# --- 4. Prompt Şablonu ---
prompt_template = """
Sen Bilim ve Teknik dergisinin Ocak 2018 sayısındaki 'Yapay Zekâ' makalesine dayalı bir asistansın.
Aşağıdaki bağlamdan yararlanarak soruya Türkçe, açık ve doğru bir yanıt ver.
Eğer bağlamda cevap varsa, sadece bağlamdan faydalanarak cevap ver.
Eğer bağlamda hiçbir bilgi yoksa "Bu bilgi makalede yer almıyor." de.

Bağlam:
{context}

Soru:
{question}
"""

prompt = PromptTemplate.from_template(prompt_template)

# --- 5. RetrievalQA Zinciri ---
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
)

print("✅ RAG pipeline başarıyla yüklendi!")

# --- 6. Export edilecek nesneler ---
__all__ = ["llm", "retriever", "qa_chain"]
