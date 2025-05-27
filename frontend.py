import streamlit as st
import requests

st.set_page_config(page_title="Smart City Info Assistant")
st.title("🏙️ Smart City Information Assistant")

query = st.text_input("Ask your question:", "")

if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        response = requests.post("http://localhost:8000/query", json={"question": query})
        result = response.json()
        st.markdown("### Answer:")
        st.success(result.get("answer", "No response"))
