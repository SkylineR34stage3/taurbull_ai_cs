# src/app/api/v1/endpoints/query.py
from fastapi import APIRouter
from pydantic import BaseModel

from src.app.core.triage import route_query

# Explanation: Create an APIRouter instance. We can add tags for OpenAPI documentation grouping.
router = APIRouter(tags=["Query"])

# --- Pydantic Model for Request Body ---
# Explanation: Defines the expected structure for data sent to the /query endpoint.
# It expects a JSON object with one key "user_query" whose value is a string.
# Inheriting from BaseModel gives us data validation superpowers via Pydantic.
class QueryRequest(BaseModel):
    user_query: str
    # Optional: We might add session_id, user_id etc. later
    # session_id: str | None = None # Python 3.10+ syntax for Optional[str]

# --- Pydantic Model for Response Body ---
# Explanation: Defines the structure for the data we'll send back.
# For now, just echoing the query and adding a dummy AI response.
class QueryResponse(BaseModel):
    original_query: str
    ai_response: str

# --- API Endpoint ---
# Explanation: Defines a POST endpoint at the root path ("/").
# When included in the main app with a prefix, this will become "/api/v1/query".
# It expects a request body matching the QueryRequest model.
# It specifies that the response will match the QueryResponse model (for documentation and validation).
@router.post("/", response_model=QueryResponse)
async def handle_query(payload: QueryRequest):
    print(f"[API Endpoint] Received query: {payload.user_query}")
    # --- Call the triage function ---
    # Explanation: Instead of generating a dummy response directly,
    # we now call our asynchronous 'route_query' function.
    # We use 'await' because route_query is an 'async def' function.
    # This pauses handle_query until route_query completes and returns its result.
    triage_result = await route_query(user_query=payload.user_query)

    print(f"[API Endpoint] Triage result: {triage_result}")

    return {
        "original_query": payload.user_query,
        "ai_response": triage_result
    }
