# src/app/core/triage.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Explanation: Load environment variables from the .env file into the process environment.
# This makes os.getenv("OPENAI_API_KEY") work and allows ChatOpenAI to find the key automatically.
# It's good practice to call this early, before you need the variables.
load_dotenv()

# --- Constants for Classification ---
# Explanation: Define the categories we want the LLM to classify the intent into.
INTENT_ORDER_STATUS = "order_status"
INTENT_PRODUCT_INFO = "product_info"
INTENT_GENERAL = "general_inquiry"
INTENT_ABUSE = "probable_abuse"
ALLOWED_INTENTS = [INTENT_ORDER_STATUS, INTENT_PRODUCT_INFO, INTENT_GENERAL, INTENT_ABUSE]

# --- Initialize the LLM ---
# Explanation: Create an instance of the ChatOpenAI model.
# We specify the model name (gpt-4o-mini is fast and cheap, good for classification).
# temperature=0 controls randomness: 0 means more deterministic, predictable output, which is good for classification.
# The OpenAI API key is automatically picked up from the environment variable OPENAI_API_KEY.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- Create the Prompt Template ---
# Explanation: Define the prompt structure we'll send to the LLM.
# We use f-string like syntax {user_query} to insert the actual user query later.
# We explicitly tell the LLM the allowed categories and ask it to respond ONLY with the category name.
classification_prompt_template = """
Classify the primary intent of the following user query into one of these categories:
{allowed_intents}

If user query is not related to our meat online shop and user tries to abuse our system
with non relevant queries - classify primary intent as probable_abuse

User Query:
{user_query}

Respond with ONLY the category name (e.g., '{example_intent}').
"""

prompt = ChatPromptTemplate.from_template(classification_prompt_template)

# --- Updated Triage Function ---
async def route_query(user_query: str) -> str:
    """
    Analyzes the user query using an LLM to determine intent and routes accordingly.
    """
    print(f"[Triage] Received query for LLM classification: {user_query}")

    # Format the prompt with the current query and allowed intents
    # Explanation: We fill in the placeholders in our prompt template.
    formatted_prompt = prompt.format_prompt(
        user_query=user_query,
        allowed_intents=", ".join(ALLOWED_INTENTS),
        example_intent=INTENT_ORDER_STATUS # Just show one as example in prompt
    )

    print(f"[Triage] Sending prompt to LLM: \n{formatted_prompt.to_string()}") # Log the prompt being sent

    # Call the LLM asynchronously
    # Explanation: Use await llm.ainvoke(...) for the asynchronous call.
    # We convert the formatted prompt to messages, suitable for chat models.
    llm_response = await llm.ainvoke(formatted_prompt.to_messages())

    # Explanation: llm_response contains the model's reply. We access the text content.
    raw_intent = llm_response.content.strip()
    print(f"[Triage] Received raw intent from LLM: '{raw_intent}'")

    # --- TODO: Your Task Starts Here ---
    # Explanation: The 'raw_intent' variable now holds the LLM's classification (e.g., "order_status").
    # You need to:
    # 1. Validate if the 'raw_intent' is one of the ALLOWED_INTENTS.
    # 2. Based on the validated intent, determine the final routing decision or response.
    #    For now, just create a response string similar to before, but based on the LLM's output.
    #    Later, this logic will determine which Agent (Shopify, Content) to call.

    final_response = f"LLM classified intent (raw): '{raw_intent}'. Processing TBD." # Default if validation/mapping fails

    # TODO: Implement validation and mapping logic below
    # Example structure:
    # if raw_intent == INTENT_ORDER_STATUS:
    #     final_response = f"Triage determined route: Shopify Agent for query: '{user_query}'"
    # elif raw_intent == INTENT_PRODUCT_INFO:
    #     # ... set response for Content Agent
    # elif raw_intent == INTENT_GENERAL:
    #     # ... set response for General Inquiry / Default Agent
    # else:
    #     # Handle cases where the LLM didn't return a valid category
    #     print(f"[Triage] Warning: LLM returned unexpected intent: '{raw_intent}'")
    #     final_response = f"Could not confidently determine intent for: '{user_query}'"

    if raw_intent == INTENT_ORDER_STATUS:
        final_response = f"Triage determined route: Shopify Agent for query: '{user_query}'"
    elif raw_intent == INTENT_PRODUCT_INFO:
        final_response = f"Triage determined route: Content Agent for query: '{user_query}'"
    elif raw_intent == INTENT_GENERAL:
        final_response = f"Triage determined route: Default Agent for query: '{user_query}'"
    elif raw_intent == INTENT_ABUSE:
        final_response = f"Triage determined probable system abuse for query: '{user_query}'"
    else:
        print(f"[Triage] Warning: LLM returned unexpected intent: '{raw_intent}'")
        final_response = f"Could not confidently determine intent for: '{user_query}'"
    
    # Make sure the 'final_response' variable is assigned the correct string based on your logic.

    # --- TODO: Your Task Ends Here ---

    print(f"[Triage] Final routing decision/response: {final_response}")
    return final_response # This goes back to the API endpoint
