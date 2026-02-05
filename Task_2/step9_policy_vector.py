from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load PDF
loader = PyPDFLoader("data/Helix_Pro_Policy_v2.pdf")
docs = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# Create embeddings
embeddings = HuggingFaceEmbeddings()

# Build vector store
db = FAISS.from_documents(chunks, embeddings)

# Test search
results = db.similarity_search("regional exceptions leave", k=2)
for i, r in enumerate(results, 1):
    print(f"\nResult {i}:\n", r.page_content[:300])
