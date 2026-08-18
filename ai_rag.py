import os
import numpy as np
import faiss
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load your hidden API key from the .env file
load_dotenv()

# Initialize the Gemini Client
client = genai.Client()

# Sample knowledge base document
chunks = [
    # "Project Apollo Overview: Launched in 2026, Project Apollo is our initiative to migrate all infrastructure to a multi-cloud environment.",
    "Project Apollo budget cap is $1.2 million. The lead engineer for this project is Dr. Sarah Jenkins.",
    "Project Zeus Overview: Project Zeus focuses on developing internal AI automation tools. It uses open-source models.",
    "Project Zeus has an expected completion date of Q4 2027. The lead manager is Marcus Vance."
]

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "gemini-embedding-2")

print(f"Generating vector embeddings using {EMBEDDING_MODEL_NAME}...")

# Request text embeddings for all chunks simultaneously
embedding_response = client.models.embed_content(
    model=EMBEDDING_MODEL_NAME,
    contents=chunks,
    config=types.EmbedContentConfig(output_dimensionality=768)
)

# Extract embedding vectors into a 2D float32 NumPy array for FAISS
embeddings = [e.values for e in embedding_response.embeddings]
embedding_matrix = np.array(embeddings).astype("float32")

# Setup Local FAISS Index (matching our 768 dimension)
dimension = embedding_matrix.shape[1] 
index = faiss.IndexFlatL2(dimension)
index.add(embedding_matrix)  # pylint: disable=no-value-for-parameter

print(f"Successfully indexed {index.ntotal} chunks into local FAISS database.")

def retrieve_relevant_chunks(query_text, top_k=2):
    query_embedding_res = client.models.embed_content(
        model=EMBEDDING_MODEL_NAME,
        contents=query_text,
        config=types.EmbedContentConfig(output_dimensionality=768)
    )
    query_vector = np.array([query_embedding_res.embeddings[0].values]).astype("float32")
    
    # Query FAISS index
    distances, indices = index.search(  # pylint: disable=no-value-for-parameter
        query_vector, top_k
    )
    print(distances, indices)

    retrieved_context = []
    for idx in indices[0]:
        if idx != -1: 
            retrieved_context.append(chunks[idx])
            
    return retrieved_context

def execute_rag_query(prompt):
    model_name = os.getenv("MODEL_NAME", "gemini-3.6-flash")
    print("\n--- Generating Final Answer via Gemini ---")
    generation_response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    return generation_response

def main():
    """Run a retrieval-augmented generation query."""
    user_query = "Who is leading Project Apollo and what is the budget?"
    print(f"\nUser Query: '{user_query}'")

    matched_contexts = retrieve_relevant_chunks(user_query, top_k=2)
    context_str = "\n".join(matched_contexts)

    rag_prompt = f"""
    You are a helpful assistant. Answer the user question accurately using only the provided context.
    If the answer is not in the context, say "I don't know".

    Context:
    {context_str}

    Question: {user_query}
    Answer:
    """

    response = execute_rag_query(rag_prompt)
    print(response.text)


if __name__ == "__main__":
    main()
