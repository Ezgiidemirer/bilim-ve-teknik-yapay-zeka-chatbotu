# 🤖 Bilim ve Teknik - Yapay Zekâ Chatbotu

## 🎯 Projenin Amacı
Bu proje, **TÜBİTAK Bilim ve Teknik Dergisi’nin Ocak 2018 sayısındaki “Yapay Zekâ” makalesine** dayalı olarak geliştirilmiş bir **RAG (Retrieval-Augmented Generation)** tabanlı chatbot’tur. 
Amaç, kullanıcıların yalnızca bu makalede yer alan bilgilere dayanarak sorularına **doğru, güvenilir ve kaynak temelli** cevaplar almasını sağlamaktır.  
Model, makale dışı konulara yanıt vermeyerek **bilgi doğruluğu** ve **kaynak güvenilirliği** ilkelerini korur.

---
## 📚 Veri Seti

Bu proje, **TÜBİTAK Bilim ve Teknik Dergisi’nin Ocak 2018 sayısında** yayımlanan  
**“Yapay Zekâ - Temel Kavramlar”** makalesine dayanmaktadır.

🔗 [Makale PDF’ini Görüntüle](./yazi.pdf)
- Sayfa Sayısı: 10
- Yazar: Gürkan Caner Birer (Bilgisayar Mühendisi)
- Yayın: TÜBİTAK Bilim ve Teknik Dergisi, Ocak 2018
- Konular:
  - Yapay zekânın tanımı ve tarihsel gelişimi  
  - Makine öğrenmesi, derin öğrenme, sinir ağları  
  - Zayıf ve güçlü yapay zekâ farkı  
  - Genetik algoritmalar  
  - Turing Testi ve donanımın önemi  
  - Büyük veri kavramı

Bu makale, chatbot’un yanıtlarını oluşturmak için kullanılan **temel bilgi kaynağıdır.**


## 📚 Veri Seti
- **Kaynak:** TÜBİTAK Bilim ve Teknik Dergisi – Ocak 2018, *“Yapay Zekâ”*
- **Format:** PDF → JSON dönüştürülmüş metin
- **İşlem Adımları:**
  - Metin çıkarımı (PyPDFLoader)
  - Temizleme ve ön işleme (regex)
  - Chunking (1500 karakterlik bağlamsal parçalara bölme)
  - Embedding ve vektör veritabanı oluşturma (ChromaDB)

---

## ⚙️ Kullanılan Teknolojiler

| Bileşen | Teknoloji | Açıklama |
|----------|------------|-----------|
| **LLM (Generation Model)** | 🧠 Google Gemini 2.5 Pro | Türkçe destekli, güvenilir yanıtlar üretir. |
| **Embedding Model** | 🔤 HuggingFace paraphrase-multilingual-MiniLM-L12-v2 | Türkçe metinleri anlam temelli vektörlere dönüştürür. |
| **Vektör Veritabanı** | 💾 ChromaDB | Metin embedding’lerini saklar ve en alakalı bölümleri getirir. |
| **Framework** | 🧩 LangChain | LLM, retriever ve prompt’u entegre eder. |
| **Web Arayüzü** | 🌐 Streamlit | Kullanıcı dostu etkileşimli arayüz sağlar. |

---

## 🧩 Mimari Akış
```
Kullanıcı → Streamlit UI → RAG Pipeline → Retriever (Chroma) → LLM (Gemini) → Cevap
```

---

## 📌 Örnek Sorular ve Cevaplar

| 💬 Soru | 🤖 Chatbot Cevabı |
|----------|-------------------|
| **1. Yapay zekâ terimini ilk kim kullandı?** | Yapay zekâ terimini ilk olarak 1956’daki Dartmouth Konferansı’nda Prof. John McCarthy kullanmıştır. |
| **2. IBM’in Deep Blue bilgisayarı neyi başardı?** | IBM’in geliştirdiği Deep Blue, 1997 yılında dünya satranç şampiyonu Garry Kasparov’u yenerek yapay zekâ tarihinde önemli bir dönüm noktası olmuştur. |
| **3. Makine öğrenmesi nedir?** | Makine öğrenmesi, açıkça programlamaya gerek kalmadan makinelerin verilerden öğrenmesini sağlayan algoritmalardır. Yapay zekânın temel yapı taşlarından biridir. |
| **4. Genetik algoritma nasıl çalışır?** | Genetik algoritmalar canlılardaki gen değişimine benzer şekilde, olası çözümler arasında en iyi sonucu verenleri seçip birleştirerek gelişir. |
| **5. Güçlü yapay zekâ ile zayıf yapay zekâ arasındaki fark nedir?** | Güçlü yapay zekâ insan kadar zeki olan sistemleri ifade ederken, zayıf yapay zekâ yalnızca belirli görevlerde uzmanlaşmıştır. |

---

## 🧮 Kurulum Adımları
```bash
pip install -r requirements.txt
python prepare_data.py
python rag_pipeline.py
streamlit run app.py
```

---

## 📁 Proje Yapısı
```
├── app.py
├── rag_pipeline.py
├── prepare_data.py
├── yapay_zeka_chunks_clean2.json
├── .env
├── requirements.txt
└── README.md
```

## 🎨 Uygulama Arayüzü

Aşağıda, chatbot arayüzünün örnek görünümü yer almaktadır:

![Chatbot Arayüzü](./images/ui_preview.png)

---

## Değerlendirme Kriterleri
 Geliştirme Ortamı (GitHub + README)  
 Veri Seti Hazırlama  
 Çalışma Kılavuzu  
 RAG Mimarisi (LangChain + Gemini + Chroma)  
 Web Arayüzü (Streamlit)

---

Bu proje, **Akbank GenAI Bootcamp** kapsamında eğitim amaçlı geliştirilmiştir.
