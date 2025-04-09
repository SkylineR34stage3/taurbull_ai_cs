# src/app/api/v1/endpoints/query.py
from fastapi import APIRouter
from pydantic import BaseModel

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
    # Explanation: 'payload' will be an instance of QueryRequest, validated by FastAPI/Pydantic.
    # We access the user's query via payload.user_query.
    # TODO: Replace this dummy logic with actual call to Triage/Agent system later.
    print(f"Received query: {payload.user_query}") # Log to server console

    dummy_ai_answer = f"I received your query about '{payload.user_query}'. I am still under development."

    # Explanation: Return a dictionary matching the QueryResponse model structure.
    # FastAPI will automatically convert this to JSON.
    return {
        "original_query": payload.user_query,
        "ai_response": dummy_ai_answer
    }
