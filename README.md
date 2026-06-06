# Sentiment Analysis API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

A machine learning-powered REST API for sentiment analysis, built with FastAPI and scikit-learn. This project performs binary sentiment classification (positive/negative) on text comments, particularly optimized for French language analysis.

## Features

- 🎯 **Binary Sentiment Classification**: Classify text as positive or negative
- 🌐 **Multi-language Support**: Trained on French language data with spaCy integration
- ⚡ **Fast REST API**: Built with FastAPI for high performance
- 🐳 **Docker Ready**: Complete Docker and Docker Compose setup
- 📊 **ML Pipeline**: Includes training notebooks and data processing tools
- 🔄 **CORS Enabled**: Pre-configured for frontend integration
- 📈 **Pre-trained Models**: Ready-to-use scikit-learn models with TF-IDF vectorization

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application entry point
│   ├── api/
│   │   └── sentiment_binaire_api.py     # Sentiment analysis endpoints
│   ├── schemas/
│   │   └── response_schema.py           # API response schema
│   └── services/
│       └── sentiments/
│           └── sentiment_comment_service.py  # Business logic
├── data/
│   ├── sentiment_data.csv               # Training data
│   └── trustpilot_reviews.csv           # Review dataset
├── ml_models/
│   └── trainings/
│       ├── first_train-model.ipynb      # Model training notebook
│       ├── initialize-data.ipynb        # Data initialization notebook
│       ├── classifier_linear_sentiment.pkl  # Pre-trained model
│       └── tfidf_vectorizer.pkl         # TF-IDF vectorizer
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Technology Stack

- **Backend Framework**: FastAPI 0.136
- **Machine Learning**: scikit-learn 1.8.0
- **NLP**: spaCy 3.8 (French language model)
- **Data Processing**: NumPy, Pandas, Scikit-learn
- **Containerization**: Docker, Docker Compose
- **Validation**: Pydantic 2.13
- **Server**: Uvicorn

## Installation

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- pip or conda

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sentimental-analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify pre-trained models are in place**
   ```
   ml_models/trainings/
   ├── classifier_linear_sentiment.pkl
   └── tfidf_vectorizer.pkl
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the API**
   The API will be available at `http://localhost:8000`

3. **View API Documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Check Sentiment (Binary Classification)

**Endpoint**: `POST /sentiments/check-comment-binary`

**Request**:
```bash
curl -X POST "http://localhost:8000/sentiments/check-comment-binary?sentence=This%20product%20is%20amazing"
```

**Query Parameters**:
- `sentence` (string, required): The text to analyze for sentiment

**Response** (200 OK):
```json
{
  "success": true,
  "message": "success",
  "data": 1
}
```

**Response Schema**:
- `success` (boolean): Indicates if the request was successful
- `message` (string): Status message
- `data` (integer): Sentiment classification (0 = negative, 1 = positive)

## Model Training

The project includes Jupyter notebooks for model training and data preparation:

1. **initialize-data.ipynb**: Data preprocessing and exploration
2. **first_train-model.ipynb**: Model training with scikit-learn

### Training Steps

1. Open the training notebooks in Jupyter
   ```bash
   jupyter notebook ml_models/trainings/
   ```

2. Run the data initialization notebook first to prepare the data

3. Run the model training notebook to train the classifier

4. Models are saved as pickle files for inference

## Data Sources

- **sentiment_data.csv**: Sentiment training dataset
- **trustpilot_reviews.csv**: Customer reviews for analysis

## Development

### Adding New Features

1. Create new endpoints in `app/api/`
2. Add data models in `app/schemas/`
3. Implement business logic in `app/services/`
4. Update `app/main.py` to register routes

### Code Structure Best Practices

- Keep API routes clean and focused
- Use schemas for request/response validation
- Implement business logic in services
- Use type hints throughout

### Environment Configuration

Create a `.env` file in the root directory for environment-specific settings:

```env
# Example environment variables
DEBUG=False
LOG_LEVEL=INFO
```

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000` (Local development)
- `http://127.0.0.1:3000` (Localhost)
- `https://demo.test.sentimental-analysis.paullence.link` (Production)

Modify `app/main.py` to add or change allowed origins.

## Troubleshooting

### Model Loading Issues

If you encounter `FileNotFoundError` for model files:
1. Ensure the pickle files exist in `ml_models/trainings/`
2. Verify the `BASE_DIR` path is correctly resolved
3. Check file permissions

### Dependencies Installation Issues

If pip install fails:
1. Upgrade pip: `pip install --upgrade pip`
2. Try installing with `--no-cache-dir` flag
3. For spaCy French model: `python -m spacy download fr_core_news_sm`

### Docker Build Issues

For Docker builds, ensure:
1. Docker daemon is running
2. Sufficient disk space available
3. Internet connection for downloading images and dependencies

## Performance Considerations

- **Inference Speed**: Models are loaded once per request; consider caching for production
- **Scalability**: Use load balancing for multiple API instances
- **Memory**: Pre-trained models consume ~50-100MB of RAM

## Future Enhancements

- [ ] Multi-class sentiment classification (positive, neutral, negative)
- [ ] Confidence scores for predictions
- [ ] Model versioning and A/B testing
- [ ] Advanced preprocessing pipeline
- [ ] Batch prediction endpoint
- [ ] Model retraining automation
- [ ] Monitoring and logging infrastructure

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add your feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact & Support

For questions or issues, please open an issue on the repository.

---

**Last Updated**: June 2026
