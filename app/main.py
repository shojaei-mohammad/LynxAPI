from fastapi import FastAPI
import uvicorn
from app.api.v1.admin import authorization

app = FastAPI()

app.include_router(authorization.router, prefix="/api/v1/admin", tags=["admin"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
