from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes.ui.default import router as default_router
app = FastAPI(
    title="Helix",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(default_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)