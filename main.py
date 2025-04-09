# main.py
from fastapi import FastAPI
from src.app.api.v1.endpoints import query as query_router_v1

# Explanation: Create an instance of the FastAPI class.
# This 'app' object will be the main point of interaction for our API.
app = FastAPI(title="Taurbull AI Customer Support", version="0.1.0")

# --- Include the API router ---
# Explanation: Mount the router we imported onto the main 'app'.
# prefix="/api/v1": All routes defined in query_router_v1 will be prefixed with /api/v1.
# So, the @router.post("/") in query.py becomes available at POST /api/v1/query.
app.include_router(query_router_v1.router, prefix="/api/v1")

# Explanation: This is a "decorator" (@app.get). It tells FastAPI that the function
# directly below it (read_root()) should handle GET requests to the specified path ("/").
# "/" is the root path of our API.
@app.get("/")
def read_root():
    # Explanation: This function is executed when a GET request hits "/".
    # It returns a Python dictionary. FastAPI automatically converts
    # this dictionary into a JSON response for the client.
    return {"message": "Support AI Backend Running"}
