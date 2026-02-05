import streamlit as st

# -------------------------------
# IMPORT BACKEND LOGIC
# -------------------------------
from question_parser import extract_emp_id, detect_intent
from app import (
    answer_structured,
    answer_policy,
    answer_hybrid
)

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# -------------------------------
# STREAMLIT CONFIG
# -------------------------------
st.set_page_config(
    page_title="Helix HR Intelligence Bot",
    layout="centered"
)

# -------- FONT SIZE REDUCTION (ONLY CHANGE) --------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    p, li, div {
        font-size: 13px !important;
        line-height: 1.4;
    }
    h3 {
        margin-bottom: 0.3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --------------------------------------------------

st.title("🧠 HELIX HR INTELLIGENCE BOT")
st.write("Ask HR questions grounded in Helix Global Corp data and policy.")


# -------------------------------
# CACHE POLICY VECTOR DB
# -------------------------------
@st.cache(allow_output_mutation=True)
def load_policy_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.load_local(
        "policy_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return db


# Load once and reuse
policy_db = load_policy_db()


# -------------------------------
# USER INPUT
# -------------------------------
question = st.text_area(
    "Ask your HR question:",
    height=140,
    placeholder="I am Gabrielle Davis (EMP1004). Based on the 2026 policy, how many annual leave days am I entitled to?"
)

submit = st.button("Get Answer")


# -------------------------------
# PROCESS QUESTION
# -------------------------------
if submit:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        emp_id = extract_emp_id(question)

        if not emp_id:
            st.error("❌ Unable to identify employee ID from the question.")
        else:
            intent = detect_intent(question)

            # Route based on intent
            if intent in [
                "annual_leave",
                "sick_leave",
                "sabbatical",
                "location_leave"
            ]:
                answer = answer_hybrid(question, emp_id)

            elif intent == "attendance":
                answer = answer_policy(question)

            else:
                answer = answer_policy(question)

            # -------------------------------
            # DISPLAY ANSWER
            # -------------------------------
            st.markdown("---")
            st.subheader("📌 Answer")
            st.write(answer)
