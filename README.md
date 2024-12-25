# mnemosyne

## Build and deploy frontend
```
gcloud run deploy mnemosyne-frontend \
  --source . \
  --target production \
  --platform managed \
  --port 8080 \
  --set-env-vars NEXT_PUBLIC_API_URL=https://your-backend-url.run.app
```

## Build and deploy backend
```
gcloud run deploy mnemosyne-backend \
  --source . \
  --target production \  # Use production stage
  --set-env-vars ENVIRONMENT=production \
  --set-secrets=...
```