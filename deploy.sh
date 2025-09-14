#!/bin/bash

# EDD Cloud Run Backend Resource Deploy Script
# Usage: ./deploy.sh [PROJECT_ID] [REGION] [SERVICE_NAME]
# 
# Configuration can be set via .env file or command line arguments
# Command line arguments override .env values

set -e

# Load .env file if it exists
if [ -f .env ]; then
    echo "Loading configuration from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Default values (can be overridden by .env file)
DEFAULT_PROJECT_ID=${PROJECT_ID:-""}
DEFAULT_REGION=${REGION:-"us-central1"}
DEFAULT_SERVICE_NAME=${SERVICE_NAME:-"edd-backend-resource"}
DEFAULT_REPO_NAME=${REPO_NAME:-"edd-hackathon-repo"}
DEFAULT_IMAGE_TAG=${IMAGE_TAG:-"latest"}
DEFAULT_MEMORY=${MEMORY:-"1Gi"}
DEFAULT_CPU=${CPU:-"1"}
DEFAULT_MAX_INSTANCES=${MAX_INSTANCES:-"10"}
DEFAULT_MIN_INSTANCES=${MIN_INSTANCES:-"0"}
DEFAULT_TIMEOUT=${TIMEOUT:-"300"}
DEFAULT_CONCURRENCY=${CONCURRENCY:-"80"}

# Parse arguments (command line overrides .env values)
PROJECT_ID=${1:-$DEFAULT_PROJECT_ID}
REGION=${2:-$DEFAULT_REGION}
SERVICE_NAME=${3:-$DEFAULT_SERVICE_NAME}
REPO_NAME=${REPO_NAME:-$DEFAULT_REPO_NAME}
IMAGE_TAG=${IMAGE_TAG:-$DEFAULT_IMAGE_TAG}
MEMORY=${MEMORY:-$DEFAULT_MEMORY}
CPU=${CPU:-$DEFAULT_CPU}
MAX_INSTANCES=${MAX_INSTANCES:-$DEFAULT_MAX_INSTANCES}
MIN_INSTANCES=${MIN_INSTANCES:-$DEFAULT_MIN_INSTANCES}
TIMEOUT=${TIMEOUT:-$DEFAULT_TIMEOUT}
CONCURRENCY=${CONCURRENCY:-$DEFAULT_CONCURRENCY}

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validate required parameters
if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "" ]; then
    echo -e "${RED}Error: PROJECT_ID is required${NC}"
    echo "Please set PROJECT_ID in .env file or pass as first argument"
    echo "Usage: ./deploy.sh [PROJECT_ID] [REGION] [SERVICE_NAME]"
    echo ""
    echo "Or create .env file:"
    echo "cp .env.example .env"
    echo "# Edit .env with your project settings"
    exit 1
fi

echo -e "${BLUE}=== EDD Cloud Run Backend Resource Deployment ===${NC}"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

# Set project
echo -e "${YELLOW}Setting GCP project...${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${YELLOW}Enabling required GCP APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Create Artifact Registry repository (if it doesn't exist)
echo -e "${YELLOW}Creating Artifact Registry repository...${NC}"
echo "Repository Name: $REPO_NAME"
gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="EDD Hackathon Docker repository" \
    || echo "Repository may already exist"

# Configure Docker to use gcloud as credential helper
echo -e "${YELLOW}Configuring Docker authentication...${NC}"
gcloud auth configure-docker $REGION-docker.pkg.dev

# Build and push the image using Cloud Build
echo -e "${YELLOW}Building and pushing Docker image using Cloud Build...${NC}"
IMAGE_URL="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME:$IMAGE_TAG"
echo "Image URL: $IMAGE_URL"

gcloud builds submit --tag $IMAGE_URL .

# Deploy to Cloud Run
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
echo "Using configuration:"
echo "  Memory: $MEMORY"
echo "  CPU: $CPU"
echo "  Max Instances: $MAX_INSTANCES"
echo "  Min Instances: $MIN_INSTANCES"
echo "  Timeout: $TIMEOUT"
echo "  Concurrency: $CONCURRENCY"
echo ""

gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_URL \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory $MEMORY \
    --cpu $CPU \
    --max-instances $MAX_INSTANCES \
    --min-instances $MIN_INSTANCES \
    --timeout $TIMEOUT \
    --concurrency $CONCURRENCY \
    --set-env-vars "PYTHON_VERSION=3.12,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,VERTEX_AI_LOCATION=$VERTEX_AI_LOCATION"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo -e "${GREEN}=== Deployment Complete! ===${NC}"
echo -e "${GREEN}Service URL: $SERVICE_URL${NC}"
echo -e "${GREEN}Health Check: $SERVICE_URL/api/v1/health${NC}"
echo -e "${GREEN}API Documentation: $SERVICE_URL/docs${NC}"
echo ""

# Test the deployment
echo -e "${YELLOW}Testing the deployment...${NC}"
if curl -f "$SERVICE_URL/api/v1/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Deployment successful!${NC}"