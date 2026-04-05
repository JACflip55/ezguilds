#!/usr/bin/env bash
# One-time GCP project setup. Run once before first deploy.
set -euo pipefail

PROJECT_ID="${1:?Usage: ./setup.sh <project-id>}"
REGION="us-central1"

echo "==> Enabling APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  cloudtasks.googleapis.com \
  firestore.googleapis.com \
  storage.googleapis.com \
  --project "$PROJECT_ID"

echo "==> Creating Cloud Storage bucket..."
gcloud storage buckets create "gs://${PROJECT_ID}-uploads" \
  --project "$PROJECT_ID" \
  --location "$REGION" \
  --uniform-bucket-level-access \
  2>/dev/null || echo "Bucket already exists"

echo "==> Creating Cloud Tasks queue..."
gcloud tasks queues create ezguilds-generate \
  --location "$REGION" \
  --project "$PROJECT_ID" \
  2>/dev/null || echo "Queue already exists"

echo "==> Creating Firestore database..."
gcloud firestore databases create \
  --location "$REGION" \
  --project "$PROJECT_ID" \
  2>/dev/null || echo "Database already exists"

echo "==> Setup complete for project: $PROJECT_ID"
