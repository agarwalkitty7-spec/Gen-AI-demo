import streamlit as st
from dotenv import load_dotenv
from groq_client import stream_groq_response
from webpage_utils import fetch_and_clean, chunk_text
from retriever import retrieve_relevant_chunks

load_dotenv()

st.set_page_config(page_title="Webpage Q&A with Groq", layout="wide")
st.title("📄 Webpage Q&A with Groq & Streamlit")

url = st.text_input("Enter webpage URL")
question = st.text_area("Ask a question about the webpage content")

if st.button("Fetch and Answer"):
    if not url.strip():
        st.error("Please enter a valid URL")
    elif not question.strip():
        st.error("Please enter a question")
    else:
        with st.spinner("Fetching webpage..."):
            page_text = fetch_and_clean(url)
        if not page_text:
            st.error("Failed to fetch or extract text from the webpage.")
        else:
            chunks = chunk_text(page_text)
            relevant_chunks = retrieve_relevant_chunks(question, chunks)

            if not relevant_chunks:
                st.warning("No relevant content found in the webpage.")
            else:
                prompt = f"Use the following context to answer the question:\n\n"
                prompt += "\n\n---\n\n".join(relevant_chunks)
                prompt += f"\n\nQuestion: {question}\nAnswer:"

                st.markdown("### Answer:")
                answer_placeholder = st.empty()
                answer = ""
                try:
                    for partial in stream_groq_response(prompt):
                        answer = partial
                        answer_placeholder.markdown(answer)
                except Exception as e:
                    st.error(f"Error getting response from Groq: {e}")
