PROJECT_ID ?= ezguilds-poc
REGION ?= us-central1
API_IMAGE = gcr.io/$(PROJECT_ID)/ezguilds-api
WORKER_IMAGE = gcr.io/$(PROJECT_ID)/ezguilds-worker

.PHONY: dev dev-api dev-worker dev-frontend deploy-api deploy-worker deploy-all teardown logs

dev-frontend:
	cd frontend && npm run dev

dev-api:
	cd api && uvicorn src.main:app --reload --port 8000

dev-worker:
	cd worker && uvicorn src.main:app --reload --port 8001

dev:
	$(MAKE) -j3 dev-frontend dev-api dev-worker

deploy-api:
	cd api && gcloud builds submit --tag $(API_IMAGE)
	gcloud run deploy ezguilds-api \
		--image $(API_IMAGE) \
		--region $(REGION) \
		--platform managed \
		--allow-unauthenticated \
		--set-env-vars="GCP_PROJECT=$(PROJECT_ID)"

deploy-worker:
	cd worker && gcloud builds submit --tag $(WORKER_IMAGE)
	gcloud run deploy ezguilds-worker \
		--image $(WORKER_IMAGE) \
		--region $(REGION) \
		--platform managed \
		--no-allow-unauthenticated \
		--set-env-vars="GCP_PROJECT=$(PROJECT_ID)"

deploy-all: deploy-api deploy-worker

teardown:
	gcloud run services delete ezguilds-api --region $(REGION) --quiet || true
	gcloud run services delete ezguilds-worker --region $(REGION) --quiet || true

logs:
	gcloud run services logs read ezguilds-api --region $(REGION) --limit 50
	gcloud run services logs read ezguilds-worker --region $(REGION) --limit 50
