# Deep Research - Google Cloud Run Deployment Makefile
PROJECT_ID = deep-research
EMAIL = 
ARTIFACT_REGISTRY_REPO = 
LOCATION = us-central1

# Service names
SERVICE_NAME = 
SERVICE_ACCOUNT_NAME = deep-research-sa
SERVICE_ACCOUNT_EMAIL = $(SERVICE_ACCOUNT_NAME)@$(PROJECT_ID).iam.gserviceaccount.com

# Image tags
IMAGE = $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(ARTIFACT_REGISTRY_REPO)/deep-research:latest

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
BLUE := \033[0;34m
NC := \033[0m

.PHONY: help setup setup-full auth build deploy clean status setup-service-account

help: ## Show this help message
	@echo "Deep Research - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

# Setup and Authentication
auth: ## Authenticate to Google Cloud
	@echo "$(GREEN)Authenticating to Google Cloud...$(NC)"
	gcloud auth login
	gcloud auth configure-docker $(LOCATION)-docker.pkg.dev

verify-service-account: ## Verify existing jupyter-agent service account
	@echo "$(GREEN)Verifying existing service account...$(NC)"
	@gcloud iam service-accounts describe $(SERVICE_ACCOUNT_EMAIL) --project=$(PROJECT_ID) --quiet || \
	(echo "$(RED)Error: Service account $(SERVICE_ACCOUNT_EMAIL) not found$(NC)" && \
	 echo "$(YELLOW)Please run 'make setup-service-account' from the jupyter-agent project first$(NC)" && \
	 exit 1)
	@echo "$(YELLOW)Ensuring service account has artifact registry access...$(NC)"
	-@gcloud projects add-iam-policy-binding $(PROJECT_ID) \
		--member="serviceAccount:$(SERVICE_ACCOUNT_EMAIL)" \
		--role="roles/artifactregistry.reader" --quiet
	@echo "$(GREEN)✓ Service account verified and configured$(NC)"

setup: ## Initial setup - create artifact registry and configure permissions
	@echo "$(GREEN)Setting up Deep Research artifact registry...$(NC)"
	@gcloud config set project $(PROJECT_ID)
	@echo "$(YELLOW)Creating deep-research artifact registry...$(NC)"
	@gcloud artifacts repositories create $(ARTIFACT_REGISTRY_REPO) \
		--repository-format=docker \
		--location=$(LOCATION) \
		--description="Docker repository for Deep Research" \
		--project=$(PROJECT_ID) --quiet || echo "Repository may already exist, continuing..."
	@echo "$(YELLOW)Setting up IAM permissions...$(NC)"
	-@gcloud projects add-iam-policy-binding $(PROJECT_ID) \
		--member="user:$(EMAIL)" \
		--role="roles/artifactregistry.writer" --quiet
	-@gcloud auth configure-docker $(LOCATION)-docker.pkg.dev --quiet

setup-full: setup verify-service-account ## Complete setup - create artifact registry and verify service account

# Build Commands
build: ## Build Docker image
	@echo "$(GREEN)Building Deep Research Docker image...$(NC)"
	docker build -t $(IMAGE) .

# Push Commands
push: ## Push image to artifact registry
	@echo "$(GREEN)Pushing image to artifact registry...$(NC)"
	docker push $(IMAGE)

# Deploy Commands
deploy: ## Deploy to Cloud Run
	@echo "$(GREEN)Deploying Deep Research to Cloud Run...$(NC)"
	gcloud run deploy $(SERVICE_NAME) \
		--image $(IMAGE) \
		--platform managed \
		--region $(LOCATION) \
		--allow-unauthenticated \
		--memory 4Gi \
		--cpu 2 \
		--min-instances 0 \
		--max-instances 10 \
		--port 8000 \
		--timeout 3600 \
		--service-account $(SERVICE_ACCOUNT_EMAIL) \
		--project $(PROJECT_ID)

# Full Pipeline Commands
deploy-full: build push deploy ## Build, push, and deploy service

# Local Development Commands
dev-local: ## Run service locally with Docker
	@echo "$(GREEN)Starting local development environment...$(NC)"
	docker run -p 8000:8000 \
		-e GOOGLE_API_KEY=$(GOOGLE_API_KEY) \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		-e ANTHROPIC_API_KEY=$(ANTHROPIC_API_KEY) \
		$(IMAGE)

dev-local-detached: ## Run service locally in background
	@echo "$(GREEN)Starting local development environment in background...$(NC)"
	docker run -d -p 8000:8000 \
		-e GOOGLE_API_KEY=$(GOOGLE_API_KEY) \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		-e ANTHROPIC_API_KEY=$(ANTHROPIC_API_KEY) \
		--name deep-research \
		$(IMAGE)

dev-stop: ## Stop local development environment
	@echo "$(GREEN)Stopping local development environment...$(NC)"
	docker stop deep-research
	docker rm deep-research

dev-python: ## Run locally with Python (requires .env file)
	@echo "$(GREEN)Starting Deep Research with Python...$(NC)"
	python main.py

# Utility Commands
status: ## Show deployment status
	@echo "$(BLUE)Deep Research - Deployment Status:$(NC)"
	@echo "Project ID: $(PROJECT_ID)"
	@echo "Location: $(LOCATION)"
	@echo "Artifact Registry: $(ARTIFACT_REGISTRY_REPO)"
	@echo "Service Account: $(SERVICE_ACCOUNT_EMAIL)"
	@echo ""
	@echo "$(YELLOW)Service URL:$(NC)"
	@gcloud run services describe $(SERVICE_NAME) --region=$(LOCATION) --format='value(status.url)' 2>/dev/null || echo "Not deployed"

registry-info: ## Show artifact registry information
	@echo "$(GREEN)Artifact Registry Information:$(NC)"
	@gcloud artifacts repositories describe $(ARTIFACT_REGISTRY_REPO) --location=$(LOCATION) 2>/dev/null || echo "Registry not found"

service-account-info: ## Show service account information
	@echo "$(GREEN)Service Account Information:$(NC)"
	@gcloud iam service-accounts describe $(SERVICE_ACCOUNT_EMAIL) --project=$(PROJECT_ID) 2>/dev/null || echo "Service account not found"

url: ## Get service URL
	@echo "$(GREEN)Service URL:$(NC)"
	@echo "$(shell gcloud run services describe $(SERVICE_NAME) --region=$(LOCATION) --format='value(status.url)' 2>/dev/null || echo 'Not deployed')"

logs: ## Show service logs
	@echo "$(GREEN)Service logs:$(NC)"
	gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$(SERVICE_NAME)" --limit=50 --format='table(timestamp,textPayload)'

clean: ## Clean local Docker images and containers
	@echo "$(GREEN)Cleaning up local Docker resources...$(NC)"
	docker system prune -f
	docker image prune -f
	-docker rmi $(IMAGE) 2>/dev/null || true

clean-cloud: ## Delete Cloud Run service
	@echo "$(RED)Deleting Cloud Run service...$(NC)"
	gcloud run services delete $(SERVICE_NAME) --region=$(LOCATION) --quiet

clean-registry: ## Delete artifact registry repository
	@echo "$(RED)Deleting artifact registry repository...$(NC)"
	gcloud artifacts repositories delete $(ARTIFACT_REGISTRY_REPO) --location=$(LOCATION) --quiet

clean-service-account: ## Delete service account and credentials
	@echo "$(RED)Deleting service account...$(NC)"
	@gcloud iam service-accounts delete $(SERVICE_ACCOUNT_EMAIL) --project=$(PROJECT_ID) --quiet

# Quick Commands
quick-deploy: ## Quick build, push, and deploy
	make build push deploy

# Health Checks
health-check: ## Check if service is healthy
	@echo "$(GREEN)Checking service health...$(NC)"
	@service_url=$$(gcloud run services describe $(SERVICE_NAME) --region=$(LOCATION) --format='value(status.url)' 2>/dev/null); \
	if [ -n "$$service_url" ]; then \
		echo "Service status: $$(curl -s -o /dev/null -w '%{http_code}' $$service_url || echo 'Failed')"; \
		echo "Service URL: $$service_url"; \
	else \
		echo "Service: Not deployed"; \
	fi