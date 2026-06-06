import pickle
from app.services.sentiments.sentiment_comment_service import SentimentService
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.response_schema import ResponseSchema
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "trainings" / "classifier_linear_sentiment.pkl"
VECTORIZER_PATH = BASE_DIR / "trainings" / "tfidf_vectorizer.pkl"


# sentiment_service = SentimentService()
router = APIRouter(
    prefix="/sentiments",
    tags=["sentiments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/check-comment-binary", response_model=ResponseSchema)
def check_sentence_sentiment(sentence: str):
    # text = sentiment_service.preprocess_text(text=sentence)
    with open (MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    with open (VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)
    text_vector = vectorizer.transform([sentence])
    result = model.predict(text_vector)
    print(result)
    return ResponseSchema(success=True,message="succes",data=result[0])