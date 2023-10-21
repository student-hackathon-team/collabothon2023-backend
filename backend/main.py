from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check_endpoint():
    return "healthy"
