# src/app/agents/content_agent.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Import our simulated retrieval tool function
from src.app.tools.retrieval_tool import get_relevant_content

load_dotenv()

# We can reuse the same LLM instance or create a new one if needed
# For now, let's assume we might want different settings potentially,
# although reusing the one from triage is also fine.
# Initialize LLM specifically for this agent (can customize settings later)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3) # Slightly more creative temp?

# --- Prompt Template for Answering Based on Context ---
# Explanation: This prompt guides the LLM to answer the user's query
# strictly based on the context we provide (from our retrieval tool).
qa_prompt_template = """
You are a helpful customer support assistant for our online shop.
Answer the user's query based ONLY on the provided context below.
If the context does not contain the answer to the query, state that clearly.
Do not make up information not present in the context.

Context:
{context}

User Query:
{user_query}

Answer:
"""
qa_prompt = ChatPromptTemplate.from_template(qa_prompt_template)

async def run_content_agent(user_query: str) -> str:
    """
    Handles content/product related queries using simulated retrieval.
    """
    print(f"[Content Agent] Received query: '{user_query}'")

    # 1. Retrieve relevant content (Simulated)
    # Explanation: Call our dummy tool to get context related to the query.
    context = await get_relevant_content(query=user_query)

    # 2. Prepare prompt for LLM
    # Explanation: Format the QA prompt with the retrieved context and original query.
    formatted_prompt = qa_prompt.format_prompt(context=context, user_query=user_query)
    print(f"[Content Agent] Sending prompt to LLM: \n{formatted_prompt.to_string()}")

    # 3. Call LLM to generate answer based on context
    # Explanation: Use await llm.ainvoke for the asynchronous call.
    llm_response = await llm.ainvoke(formatted_prompt.to_messages())
    final_answer = llm_response.content.strip()

    print(f"[Content Agent] Generated final answer: '{final_answer}'")
    return final_answer
