#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${1:?Usage: ./teardown.sh <project-id>}"
REGION="us-central1"

echo "==> Deleting Cloud Run services..."
gcloud run services delete ezguilds-api --region "$REGION" --project "$PROJECT_ID" --quiet 2>/dev/null || true
gcloud run services delete ezguilds-worker --region "$REGION" --project "$PROJECT_ID" --quiet 2>/dev/null || true

echo "==> Deleting Cloud Tasks queue..."
gcloud tasks queues delete ezguilds-generate --location "$REGION" --project "$PROJECT_ID" --quiet 2>/dev/null || true

echo "==> Deleting Cloud Storage bucket..."
gcloud storage rm -r "gs://${PROJECT_ID}-uploads" 2>/dev/null || true

echo "==> Teardown complete. Firestore database left intact (manual deletion required)."
