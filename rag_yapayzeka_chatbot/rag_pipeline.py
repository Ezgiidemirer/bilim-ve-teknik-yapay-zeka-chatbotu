# rag_pipeline.py

import os
import json
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# --- .env dosyasını yükle ---
load_dotenv()

# --- Google API anahtarı ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY .env dosyasında bulunamadı!")
os.environ["GOOGLE_API_KEY"] = api_key

# --- 1. Veri Yükleme ---
with open("yapay_zeka_chunks_clean2.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

docs = [
    Document(page_content=c["content"], metadata={"page": c.get("page", None)})
    for c in chunks
]

# --- 2. Embedding ve Vektör Veritabanı ---
embedding = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

# Eğer veritabanı mevcutsa yeniden embedding yapma
if not os.path.exists("chroma_db"):
    print("🔍 Yeni embedding veritabanı oluşturuluyor...")
    vectorstore = Chroma.from_documents(docs, embedding, persist_directory="chroma_db")
    vectorstore.persist()
else:
    print("📁 Var olan embedding veritabanı yükleniyor...")
    vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embedding)

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
llm = GoogleGenerativeAI(model="gemini-2.5-pro")
retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
)

print("✅ RAG pipeline başarıyla yüklendi!")

# --- 6. Export edilecek nesneler ---
__all__ = ["llm", "retriever", "qa_chain"]
