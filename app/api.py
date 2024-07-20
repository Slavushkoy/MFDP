from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes.regressor_predict import model_router


app = FastAPI(from_attributes=True)


@app.get("/")
async def home():
    return RedirectResponse(url="/docs")


# Register routes
app.include_router(model_router, prefix="/model")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

