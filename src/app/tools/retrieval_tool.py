# src/app/tools/retrieval_tool.py

# Explanation: This module will eventually contain the actual RAG logic
# interacting with Scrapy and Pinecone. For now, it simulates retrieval.

async def get_relevant_content(query: str) -> str:
    """
    Simulates retrieving relevant content for a query.
    Replace this with actual RAG implementation later.
    """
    print(f"[Retrieval Tool] Simulating content retrieval for query: '{query}'")
    query_lower = query.lower()
    context = "No specific content found in knowledge base for this query." # Default response

    # --- TODO: Your Task Starts Here ---
    # Explanation: Add simple keyword-based logic to return different
    # hardcoded context strings based on the user's query.
    # This simulates finding relevant documents in a vector database.

    # Define keyword lists for each category
    warranty_keywords = ["warranty", "guarantee"]
    return_keywords = ["return", "returns", "refund"]
    shipping_keywords = ["shipping", "delivery", "ship"]
    ingredient_keywords = ["ingredients", "ingredient", "allergens", "contains"]
    storage_keywords = ["storage", "store", "keep"]

    # Check if any of the keywords in each category are in the query
    if any(keyword in query_lower for keyword in warranty_keywords):
        context = "Our standard product warranty is 1 year for manufacturing defects. Extended warranties can be purchased separately."
    elif any(keyword in query_lower for keyword in return_keywords):
        context = "You can return unused items within 30 days for a full refund. Please visit our returns page for details."
    elif any(keyword in query_lower for keyword in shipping_keywords):
        context = "Standard shipping takes 3-5 business days. Express shipping is available for an additional fee."
    elif any(keyword in query_lower for keyword in ingredient_keywords):
        context = "The product contains the following ingredients: [list of ingredients]"
    elif any(keyword in query_lower for keyword in storage_keywords):
        context = "Store in a cool, dry place away from direct sunlight. Keep out of reach of children."

    print(f"[Retrieval Tool] Simulated context found: '{context[:100]}...'") # Log snippet
    return context
