from fastapi import FastAPI
from app.api.sentiment_binaire_api import router as sentiment_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(sentiment_router)
origins = [
    "http://localhost:3000",      # React local development port
    "http://127.0.0.1:3000",
    "https://demo.test.sentimental-analysis.paullence.link",    # Production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # List of allowed origins
    allow_credentials=True,           # Allow cookies and auth headers
    allow_methods=["*"],             # Allow all standard HTTP methods
    allow_headers=["*"],             # Allow all standard custom headers
)