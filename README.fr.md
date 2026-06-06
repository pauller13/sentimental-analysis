# API d'Analyse de Sentiment

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Supporté-blue.svg)](https://www.docker.com/)

Une API REST alimentée par l'apprentissage automatique pour l'analyse de sentiments, construite avec FastAPI et scikit-learn. Ce projet effectue une classification de sentiments binaire (positif/négatif) sur des commentaires textuels, particulièrement optimisée pour l'analyse en langue française.

## Caractéristiques

- 🎯 **Classification de Sentiments Binaire**: Classez le texte comme positif ou négatif
- 🌐 **Support Multilingue**: Entraîné sur des données en français avec intégration spaCy
- ⚡ **API REST Rapide**: Construit avec FastAPI pour des performances élevées
- 🐳 **Prêt pour Docker**: Configuration complète Docker et Docker Compose
- 📊 **Pipeline ML**: Inclut des notebooks d'entraînement et des outils de traitement de données
- 🔄 **CORS Activé**: Pré-configuré pour l'intégration du frontend
- 📈 **Modèles Pré-entraînés**: Modèles scikit-learn prêts à l'emploi avec vectorisation TF-IDF

## Structure du Projet

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                          # Point d'entrée de l'application FastAPI
│   ├── api/
│   │   └── sentiment_binaire_api.py     # Points de terminaison d'analyse de sentiments
│   ├── schemas/
│   │   └── response_schema.py           # Schéma de réponse API
│   └── services/
│       └── sentiments/
│           └── sentiment_comment_service.py  # Logique métier
├── data/
│   ├── sentiment_data.csv               # Données d'entraînement
│   └── trustpilot_reviews.csv           # Ensemble de données d'avis
├── ml_models/
│   └── trainings/
│       ├── first_train-model.ipynb      # Notebook d'entraînement du modèle
│       ├── initialize-data.ipynb        # Notebook d'initialisation des données
│       ├── classifier_linear_sentiment.pkl  # Modèle pré-entraîné
│       └── tfidf_vectorizer.pkl         # Vectoriseur TF-IDF
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.fr.md
```

## Pile Technologique

- **Framework Backend**: FastAPI 0.136
- **Apprentissage Automatique**: scikit-learn 1.8.0
- **Traitement du Langage Naturel**: spaCy 3.8 (modèle langue française)
- **Traitement de Données**: NumPy, Pandas, Scikit-learn
- **Conteneurisation**: Docker, Docker Compose
- **Validation**: Pydantic 2.13
- **Serveur**: Uvicorn

## Installation

### Prérequis

- Python 3.11+
- Docker & Docker Compose (optionnel)
- pip ou conda

### Configuration Locale

1. **Clonez le référentiel**
   ```bash
   git clone <url-du-référentiel>
   cd sentimental-analysis
   ```

2. **Créez un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installez les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Vérifiez que les modèles pré-entraînés sont en place**
   ```
   ml_models/trainings/
   ├── classifier_linear_sentiment.pkl
   └── tfidf_vectorizer.pkl
   ```

5. **Exécutez l'application**
   ```bash
   uvicorn app.main:app --reload
   ```
   L'API sera disponible à `http://localhost:8000`

### Configuration Docker

1. **Construisez et exécutez avec Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Accédez à l'API**
   L'API sera disponible à `http://localhost:8000`

3. **Consultez la Documentation de l'API**
   - Interface Swagger: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Points de Terminaison de l'API

### Vérifier le Sentiment (Classification Binaire)

**Point de terminaison**: `POST /sentiments/check-comment-binary`

**Requête**:
```bash
curl -X POST "http://localhost:8000/sentiments/check-comment-binary?sentence=Ce%20produit%20est%20fantastique"
```

**Paramètres de Requête**:
- `sentence` (chaîne, requis): Le texte à analyser pour le sentiment

**Réponse** (200 OK):
```json
{
  "success": true,
  "message": "succès",
  "data": 1
}
```

**Schéma de Réponse**:
- `success` (booléen): Indique si la requête a réussi
- `message` (chaîne): Message de statut
- `data` (entier): Classification du sentiment (0 = négatif, 1 = positif)

## Entraînement du Modèle

Le projet inclut des notebooks Jupyter pour l'entraînement du modèle et la préparation des données:

1. **initialize-data.ipynb**: Prétraitement et exploration des données
2. **first_train-model.ipynb**: Entraînement du modèle avec scikit-learn

### Étapes d'Entraînement

1. Ouvrez les notebooks d'entraînement dans Jupyter
   ```bash
   jupyter notebook ml_models/trainings/
   ```

2. Exécutez d'abord le notebook d'initialisation des données pour préparer les données

3. Exécutez le notebook d'entraînement du modèle pour entraîner le classificateur

4. Les modèles sont enregistrés en tant que fichiers pickle pour l'inférence

## Sources de Données

- **sentiment_data.csv**: Ensemble de données d'entraînement des sentiments
- **trustpilot_reviews.csv**: Avis des clients pour l'analyse

## Développement

### Ajouter de Nouvelles Fonctionnalités

1. Créez de nouveaux points de terminaison dans `app/api/`
2. Ajoutez des modèles de données dans `app/schemas/`
3. Implémentez la logique métier dans `app/services/`
4. Mettez à jour `app/main.py` pour enregistrer les routes

### Bonnes Pratiques de Structure de Code

- Gardez les routes API propres et ciblées
- Utilisez les schémas pour la validation des requêtes/réponses
- Implémentez la logique métier dans les services
- Utilisez les indications de type partout

### Configuration de l'Environnement

Créez un fichier `.env` dans le répertoire racine pour les paramètres spécifiques à l'environnement:

```env
# Exemples de variables d'environnement
DEBUG=False
LOG_LEVEL=INFO
```

## Configuration CORS

L'API est configurée pour accepter les requêtes provenant de:
- `http://localhost:3000` (Développement local)
- `http://127.0.0.1:3000` (Localhost)
- `https://demo.test.sentimental-analysis.paullence.link` (Production)

Modifiez `app/main.py` pour ajouter ou modifier les origines autorisées.

## Dépannage

### Problèmes de Chargement du Modèle

Si vous rencontrez `FileNotFoundError` pour les fichiers de modèle:
1. Assurez-vous que les fichiers pickle existent dans `ml_models/trainings/`
2. Vérifiez que le chemin `BASE_DIR` est correctement résolu
3. Vérifiez les autorisations d'accès aux fichiers

### Problèmes d'Installation des Dépendances

Si l'installation via pip échoue:
1. Mettez à jour pip: `pip install --upgrade pip`
2. Essayez d'installer avec le drapeau `--no-cache-dir`
3. Pour le modèle français spaCy: `python -m spacy download fr_core_news_sm`

### Problèmes de Build Docker

Pour les builds Docker, assurez-vous que:
1. Le démon Docker est en cours d'exécution
2. Il y a suffisamment d'espace disque disponible
3. Connexion Internet pour télécharger les images et dépendances

## Considérations de Performance

- **Vitesse d'Inférence**: Les modèles sont chargés une fois par requête; envisagez la mise en cache pour la production
- **Scalabilité**: Utilisez l'équilibrage de charge pour plusieurs instances d'API
- **Mémoire**: Les modèles pré-entraînés consomment ~50-100MB de RAM

## Améliorations Futures

- [ ] Classification de sentiments multi-classe (positif, neutre, négatif)
- [ ] Scores de confiance pour les prédictions
- [ ] Versioning des modèles et test A/B
- [ ] Pipeline de prétraitement avancé
- [ ] Point de terminaison pour prédictions par lot
- [ ] Automatisation du réentraînement du modèle
- [ ] Infrastructure de suivi et journalisation

## Contribution

1. Créez une branche de fonctionnalité: `git checkout -b feature/votre-fonctionnalité`
2. Validez les modifications: `git commit -m 'Ajoutez votre fonctionnalité'`
3. Poussez vers la branche: `git push origin feature/votre-fonctionnalité`
4. Soumettez une demande de tirage

## Licence

Ce projet est sous licence MIT - consultez le fichier LICENSE pour les détails.

## Contact et Support

Pour toute question ou problème, veuillez ouvrir un problème sur le référentiel.

---

**Dernière mise à jour**: Juin 2026
