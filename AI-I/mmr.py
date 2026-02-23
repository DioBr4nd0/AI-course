import warnings
warnings.filterwarnings("ignore")

from datasets import load_dataset
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pprint import pprint

print("Loading 1 Lakh (100,000) news articles...")
# Using ag_news: A massive dataset of real news articles 
dataset = load_dataset("ag_news", split="train[:100000]")

docs = [Document(page_content=row['text'], metadata={"label": row['label']}) 
        for row in dataset if row['text'].strip() != ""]

print("Initializing embeddings on Nvidia GPU (CUDA)...")
# Since you are on your Nvidia PC, this forces the model to use your GPU, 
# cutting the embedding time for 100k items from an hour down to minutes.
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cuda'}
)

print("Building FAISS index (This will take a moment for 100k items)...")
vectorstore = FAISS.from_documents(docs, embeddings)

# A highly reported event guaranteed to have dozens of redundant articles
query = "What happened with the Oracle takeover bid for PeopleSoft?"

# --- STANDARD RAG: The Expensive Way ---
# We have to fetch 10 chunks just to try and get the full story
standard_retriever = vectorstore.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 10} 
)
standard_results = standard_retriever.invoke(query)

# --- MMR RAG: The Cheap, Smart Way ---
# We only fetch 3 chunks, slashing our LLM token costs by 70%
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr", 
    search_kwargs={"k": 3, "fetch_k": 30, "lambda_mult": 0.6}
)
mmr_results = mmr_retriever.invoke(query)

print("\n" + "="*60)
print("🔍 STANDARD RAG (Sending 10 chunks to the LLM = HIGH COST)")
print("="*60)
for i, doc in enumerate(standard_results): # Printing top 3 for brevity
    print(f"\n--- Result {i+1} ---")
    pprint(doc.page_content)
print("\n... plus 7 more highly similar chunks sent to the LLM.")

print("\n" + "="*60)
print("🔀 MMR RAG (Sending 3 diverse chunks to the LLM = LOW COST)")
print("="*60)
for i, doc in enumerate(mmr_results):
    print(f"\n--- Result {i+1} ---")
    pprint(doc.page_content)