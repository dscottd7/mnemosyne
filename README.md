# mnemosyne

## Deploy locally

```
docker compose build  # build
docker compose up  # start
docker compose down  # destroy
docker network prune -f  # clean up
```

## Deploy to Google Cloud

### Build
```
docker compose build  # build
```

### Deploy frontend
```
gcloud run deploy mnemosyne-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars=NEXT_PUBLIC_API_URL=https://mnemosyne-backend-302656282665.us-central1.run.app
```

### Deploy backend
```
gcloud run deploy mnemosyne-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets=OPENAI_API_KEY=OPENAI_API_KEY:latest,PINECONE_API_KEY=PINECONE_API_KEY:latest,PINECONE_ENV=PINECONE_ENV:latest,PINECONE_INDEX_NAME=PINECONE_INDEX_NAME:latest,PINECONE_HOST=PINECONE_HOST:latest \
  --set-env-vars=ENVIRONMENT=production
```