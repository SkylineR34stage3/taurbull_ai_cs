# main.py
from fastapi import FastAPI

# Explanation: Create an instance of the FastAPI class.
# This 'app' object will be the main point of interaction for our API.
app = FastAPI()

# Explanation: This is a "decorator" (@app.get). It tells FastAPI that the function
# directly below it (read_root()) should handle GET requests to the specified path ("/").
# "/" is the root path of our API.
@app.get("/")
def read_root():
    # Explanation: This function is executed when a GET request hits "/".
    # It returns a Python dictionary. FastAPI automatically converts
    # this dictionary into a JSON response for the client.
    return {"message": "Support AI Backend Running"}

# Explanation: This is another endpoint, just for demonstration.
# It handles GET requests to the path "/hello".
@app.get("/hello")
def read_hello():
    return {"greeting": "Hello from your IT Mentor!"}