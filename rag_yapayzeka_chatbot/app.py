import sys, os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
from rag_pipeline import llm, retriever, qa_chain
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA


# --- Streamlit Ayarları ---
st.set_page_config(page_title="Bilim ve Teknik - Yapay Zeka Chatbotu", page_icon="🤖")
st.title("🤖 Bilim ve Teknik - Yapay Zeka Chatbotu")
st.caption("Sadece makale içeriğine göre yanıt verir.")

# --- Prompt Şablonu ---
prompt_template = """
Sen Bilim ve Teknik dergisinin Ocak 2018 sayısındaki 'Yapay Zeka' makalesine dayalı bir asistansın.
Yalnızca makalede geçen bilgilerle cevap ver.

Bağlamda sorunun cevabı açıkça geçiyorsa, o bilgiyi kullanarak net, kısa ve anlaşılır bir Türkçe cevap ver.
Bağlamda cevap yoksa ya da konu makale dışında kalıyorsa:
"Bu bilgi makalede yer almıyor çünkü soru makale içeriğiyle doğrudan ilgili değil." de.

Bağlam:
{context}

Soru:
{question}
"""
prompt = PromptTemplate.from_template(prompt_template)

# --- QA Zinciri ---
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
)

# --- Kullanıcı Arayüzü ---
question = st.text_input("🔎 Bir soru sor:", placeholder="Örn: IBM’in Deep Blue bilgisayarı hangi yıl Kasparov’u yendi?")

if st.button("Cevapla"):
    if not question.strip():
        st.warning("⚠ Lütfen bir soru yaz!")
    else:
        with st.spinner("🧠 Yapay zeka düşünüyor..."):
            try:
                # 🔍 Önce hangi chunk'lar bulunduğunu göster
                st.subheader("📚 İlgili Metin Parçaları")
                docs = retriever.get_relevant_documents(question)
                for i, d in enumerate(docs, 1):
                    st.text(f"{i}. (Sayfa {d.metadata.get('page')}): {d.page_content[:300]}...\n")

                # 🔮 Sonra LLM cevabı üret
                answer = qa_chain.run(question)

                st.subheader("💬 Cevap")
                if "Bu bilgi makalede yer almıyor" in answer:
                    st.warning(answer)
                else:
                    st.success(answer)

            except Exception as e:
                st.error("❌ Bir hata oluştu.")
                st.text(str(e))

st.markdown("---")
st.caption("📖 Kaynak: TÜBİTAK Bilim ve Teknik Dergisi - Ocak 2018, 'Yapay Zekâ' makalesi")
