# src/app/tools/retrieval_tool.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec, PodSpec # Make sure PodSpec is imported if using provisioned index
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# --- Initialize Embeddings Model ---
# Explanation: Using OpenAI's embedding model. LangChain handles fetching the API key.
# Make sure OPENAI_API_KEY is set in your .env
embeddings = OpenAIEmbeddings(model="text-embedding-3-small") # Or another model

# --- Initialize Pinecone ---
# Explanation: Fetch Pinecone credentials from environment variables.
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

if not all([PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME]):
    raise ValueError("Pinecone API Key, Environment, or Index Name not found in environment variables.")

# Initialize Pinecone client (using the native client is often recommended now)
pinecone = Pinecone(api_key=PINECONE_API_KEY) # Environment might not be needed directly for newer client versions depending on context

# Check if index exists, create if not (Optional: good for first run)
# NOTE: Index creation via API might take time and is often done manually first.
# if PINECONE_INDEX_NAME not in pinecone.list_indexes().names:
#     print(f"Creating Pinecone index: {PINECONE_INDEX_NAME}")
#     # Define spec based on your index type (Serverless or Pod)
#     # Example for Serverless:
#     spec = ServerlessSpec(cloud='aws', region='us-west-2') # Adjust cloud/region
#     # Example for Pod (e.g., p1.x1 instance):
#     # spec = PodSpec(environment=PINECONE_ENVIRONMENT, pod_type='p1.x1', pods=1) # Adjust environment/pod_type
#     pinecone.create_index(
#         PINECONE_INDEX_NAME,
#         dimension=1536, # MUST match your embedding model's dimension (e.g., 1536 for text-embedding-3-small)
#         metric='cosine',
#         spec=spec
#     )
#     print("Index creation initiated. Please wait a moment for it to initialize.")
#     # time.sleep(60) # Wait for index to be ready (crude)

# --- Initialize LangChain Pinecone Vector Store ---
# Explanation: Connect LangChain to your Pinecone index using the embeddings model.
# This object allows searching the index.
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings
)

async def get_relevant_content(query: str, k: int = 3) -> str:
    """
    Retrieves relevant content for a query from Pinecone vector store.
    """
    print(f"[Retrieval Tool] Retrieving content for query: '{query}'")

    context = ""

    try:
        retrieved_docs = await vectorstore.asimilarity_search(query, k=k)
        if not retrieved_docs:
            context = "No relevant content found in knowledge base."
        else:
            context = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
            print(f"[Retrieval Tool] Found {len(retrieved_docs)} relevant document(s).")
    except Exception as e:
        print(f"[Retrieval Tool] Error during similarity search: {e}")

    print(f"[Retrieval Tool] Retrieved context snippet: '{context[:100]}...'")
    return context
