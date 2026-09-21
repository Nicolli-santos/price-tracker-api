from fastapi import FastAPI

app = FastAPI(title="Price Tracker API")

@app.get("/")
def read_root():
    return {"message": "Price Tracker API is running!"}