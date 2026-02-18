import ollama
import chromadb


def load_chunk(filename):
    with open(filename,'r') as f:
        text = f.read()
    
    chunks = text.split('\n\n')
    return [chunk.strip() for chunk in chunks if chunk.strip()]
# 2. Setup Database
client = chromadb.Client()
collection = client.create_collection(name="demo")

# 3. Store Data (Embed -> Store)
# for i, d in enumerate(docs):
#     response = ollama.embeddings(model="dolphin-phi:latest", prompt=d)
#     collection.add(ids=[str(i)], embeddings=[response["embedding"]], documents=[d])

# 4. User Asks Question
question = "What do llamas eat?"
print(f"Question: {question}")

# 5. Retrieve Relevant Data
q_response = ollama.embeddings(model="dolphin-phi:latest", prompt=question)
results = collection.query(query_embeddings=[q_response["embedding"]], n_results=1)
context = results['documents'][0][0]
print(f"Found relevant info: {context}")

# 6. Generate Answer
# prompt = f"Using this data: {context}. Answer this: {question}"
# output = ollama.generate(model="dolphin-phi:latest", prompt=prompt)

filename = "knowledge.txt"
documents = load_chunk(filename)

print("embedding chunks")
for i, chunk in enumerate(documents):
    response = ollama.embeddings(model="dolphin-phi:latest", prompt=chunk)
    embedding = response["embedding"]

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk]
    )

print("storage complete")

question = "how big is the pretty mirror?"

response = ollama.embeddings(model = "dolphin-phi:latest", prompt = question)
question_embedding = response["embedding"]

results = collection.query(query_embeddings= [question_embedding], n_results = 1)

retrived_text = results['documents'][0][0]
print(retrived_text)