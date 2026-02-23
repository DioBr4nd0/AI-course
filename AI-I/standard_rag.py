import warnings
warnings.filterwarnings("ignore")

from datasets import load_dataset
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pprint import pprint

print("Loading dataset...")
dataset = load_dataset("databricks/databricks-dolly-15k", split="train[:1000]")


docs = [Document(page_content=row['context'], metadata={"category": row['category']}) 
        for row in dataset if row['context'].strip() != ""]

print("Initializing embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


print("Building FAISS index...")
vectorstore = FAISS.from_documents(docs, embeddings)

query = "Explain the concepts of machine learning and artificial intelligence."

standard_retriever = vectorstore.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 3}
)
standard_results = standard_retriever.invoke(query)

mmr_retriever = vectorstore.as_retriever(
    search_type="mmr", 
    search_kwargs={"k": 3, "fetch_k": 15, "lambda_mult": 0.5}
)
mmr_results = mmr_retriever.invoke(query)

print("\n" + "="*60)
print("🔍 STANDARD RAG RESULTS (Similarity Only)")
print("="*60)
for i, doc in enumerate(standard_results):
    print(f"\n--- Result {i+1} ---")
    pprint(doc.page_content[:250] + "...") # Truncated for readability

print("\n" + "="*60)
print("🔀 MMR RAG RESULTS (Similarity + Diversity)")
print("="*60)
for i, doc in enumerate(mmr_results):
    print(f"\n--- Result {i+1} ---")
    pprint(doc.page_content[:250] + "...")