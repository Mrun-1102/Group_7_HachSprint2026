import streamlit as st
import pandas as pd
from app.storage.mongo_client import MongoClient
from app.rag.chatbot import NewsChatbot
import time

st.set_page_config(page_title="NewsStream AI Intelligence", layout="wide", page_icon="📰")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .news-card { background-color: #1e2130; padding: 20px; border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #00d4ff; }
    h1, h2, h3 { color: #00d4ff; }
    .chatbot-msg { background-color: #262730; padding: 15px; border-radius: 10px; margin-top: 10px; border: 1px solid #3e404b; color: #fff; }
    .source-link { color: #00d4ff; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📰 NewsStream AI – Real-Time Intelligence")

# Sidebar
st.sidebar.title("System Controls")
if st.sidebar.button("🔄 Sync Live Feeds (TimeWatcher)"):
    with st.spinner("Executing Data Pipeline..."):
        from app.api.pipeline import run_pipeline
        duration, count = run_pipeline()
    st.sidebar.success(f"Sync Complete! Processed {count} articles in {duration:.2f}s")

# Data Loading
db = MongoClient()
articles = db.get_all_articles()
df = pd.DataFrame(articles)

if not df.empty:
    # 1. Metrics Section
    st.header("📊 Intelligence Real-Time Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_articles = len(df)
    categories = df['category'].value_counts()
    
    col1.metric("Total Stories", total_articles)
    col2.metric("Most Active Topic", categories.index[0] if not categories.empty else "N/A")
    col3.metric("Insight Categories", df['category'].nunique())
    col4.metric("Sources Tracked", df['source'].nunique())

    st.markdown("---")
    
    # 2. RAG Chatbot Q&A
    st.header("🤖 NewsStream Q&A AI (Knowledge-Grounded)")
    chatbot = NewsChatbot()
    
    query = st.text_input("Ask a question about the latest news:", placeholder="e.g. Give me the top 5 latest news with links.")
    
    if query:
        with st.spinner("Retrieving from intelligence pool..."):
            answer, sources = chatbot.ask(query)
            
            st.markdown("### 📝 AI Answer")
            st.markdown(f'<div class="chatbot-msg">{answer}</div>', unsafe_allow_html=True)
            
            if sources:
                st.markdown("#### 🔗 Referenced Sources")
                for src in sources:
                    st.markdown(f"- <a class='source-link' href='{src['url']}' target='_blank'>{src['title']}</a>", unsafe_allow_html=True)

    st.markdown("---")

    # 3. News Feed
    st.header("🗞️ Latest Scraped Headlines")
    
    # Sort
    if 'processed_at' in df.columns:
        sorted_df = df.sort_values(by='processed_at', ascending=False)
    else:
        sorted_df = df
        
    for _, row in sorted_df.iterrows():
        # Pre-process content snippet to avoid f-string backslash error
        title = row.get('title', 'No Title')
        source = row.get('source', 'Unknown')
        category = row.get('category', 'General')
        url = row.get('url', '#')
        
        summary_text = row.get('summary')
        if not summary_text:
            content = row.get('content', '')
            summary_text = content[:250].replace('\n', ' ') + '...'
            
        with st.container():
            st.markdown(f"""
            <div class="news-card">
                <h3 style='margin-top:0;'>{title}</h3>
                <p style='color:#00d4ff;'>Source: {source} | Topic: {category}</p>
                <p style='color:#ccc;'>{summary_text}</p>
                <a class='source-link' href="{url}" target="_blank">🔗 Full Article Link</a>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Full Intelligence & Summary"):
                st.subheader("Summary")
                st.write(row.get('summary', 'No summary available.'))
                st.subheader("Full Content")
                st.write(row.get('content', 'No content available.'))

else:
    st.info("System initializing. Click 'Sync Live Feeds' in the sidebar to populate intelligence.")

# Footer
st.markdown("---")
st.markdown("Developed for HackSprint | NewsStream AI Engine © 2026")
