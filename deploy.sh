#!/bin/bash

# Exit on any error
set -e

PROJECT_ID="mnemosyne-gpt"
REGION="us-central1"
BACKEND_SERVICE="mnemosyne-backend"
FRONTEND_SERVICE="mnemosyne-frontend"

echo "Deploying backend..."

# Build and deploy backend using cloudbuild.yaml
gcloud builds submit backend/ \
    --config backend/cloudbuild.yaml \
    --project $PROJECT_ID

# Deploy the backend to Cloud Run with additional configuration
gcloud run deploy $BACKEND_SERVICE \
    --image gcr.io/$PROJECT_ID/$BACKEND_SERVICE \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --timeout 300 \
    --min-instances 1 \
    --max-instances 10 \
    --set-env-vars="OPENAI_API_KEY=${OPENAI_API_KEY},PINECONE_API_KEY=${PINECONE_API_KEY},PINECONE_ENV=${PINECONE_ENV},PINECONE_INDEX_NAME=${PINECONE_INDEX_NAME},PINECONE_HOST=${PINECONE_HOST}" \
    --project $PROJECT_ID \
    --cpu-boost \
    --execution-environment=gen2

# Get the backend URL for the frontend configuration
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --region $REGION --format='value(status.url)')

echo "Backend deployed at: $BACKEND_URL"

echo "Deploying frontend..."

# Create frontend build configuration
cat > frontend/cloudbuild.yaml << EOF
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build',
           '--build-arg', 'NEXT_PUBLIC_API_URL=${BACKEND_URL}',
           '-t', 'gcr.io/\$PROJECT_ID/${FRONTEND_SERVICE}',
           '.']
images: ['gcr.io/\$PROJECT_ID/${FRONTEND_SERVICE}']
EOF

# Build and deploy frontend
gcloud builds submit frontend/ \
    --config frontend/cloudbuild.yaml \
    --project $PROJECT_ID

# Deploy frontend to Cloud Run
gcloud run deploy $FRONTEND_SERVICE \
    --image gcr.io/$PROJECT_ID/$FRONTEND_SERVICE \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}" \
    --project $PROJECT_ID

echo "Deployment complete!"