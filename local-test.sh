#!/bin/bash

# EDD Cloud Run Backend Resource Local Test Script
# Usage: ./local-test.sh [build|run|test|stop|clean]

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="edd-backend-resource"
CONTAINER_NAME="edd-backend-resource-local"
PORT=8080

# Functions
build_image() {
    echo -e "${YELLOW}Building Docker image...${NC}"
    docker build -t $IMAGE_NAME .
    echo -e "${GREEN}✓ Docker image built successfully${NC}"
}

run_container() {
    echo -e "${YELLOW}Running container locally...${NC}"
    
    # Stop existing container if running
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    
    # Run new container
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:8080 \
        -e PORT=8080 \
        $IMAGE_NAME
    
    echo -e "${GREEN}✓ Container started successfully${NC}"
    echo -e "${GREEN}Application URL: http://localhost:$PORT${NC}"
    echo -e "${GREEN}Health Check: http://localhost:$PORT/api/v1/health${NC}"
    echo -e "${GREEN}API Docs: http://localhost:$PORT/docs${NC}"
    
    # Wait for container to be ready
    echo -e "${YELLOW}Waiting for container to be ready...${NC}"
    sleep 5
}

test_endpoints() {
    echo -e "${YELLOW}Testing API endpoints...${NC}"
    
    # Test root endpoint
    echo -e "${BLUE}Testing root endpoint...${NC}"
    if curl -f "http://localhost:$PORT/" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Root endpoint is working${NC}"
    else
        echo -e "${RED}✗ Root endpoint failed${NC}"
        return 1
    fi
    
    # Test health endpoint
    echo -e "${BLUE}Testing health endpoint...${NC}"
    if curl -f "http://localhost:$PORT/api/v1/health/" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Health endpoint is working${NC}"
    else
        echo -e "${RED}✗ Health endpoint failed${NC}"
        return 1
    fi
    
    # Test liveness probe
    echo -e "${BLUE}Testing liveness probe...${NC}"
    if curl -f "http://localhost:$PORT/api/v1/health/liveness" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Liveness probe is working${NC}"
    else
        echo -e "${RED}✗ Liveness probe failed${NC}"
        return 1
    fi
    
    # Test readiness probe
    echo -e "${BLUE}Testing readiness probe...${NC}"
    if curl -f "http://localhost:$PORT/api/v1/health/readiness" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Readiness probe is working${NC}"
    else
        echo -e "${RED}✗ Readiness probe failed${NC}"
        return 1
    fi
    
    # Test API info endpoint
    echo -e "${BLUE}Testing API info endpoint...${NC}"
    if curl -f "http://localhost:$PORT/api/v1/info" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ API info endpoint is working${NC}"
    else
        echo -e "${RED}✗ API info endpoint failed${NC}"
        return 1
    fi
    
    echo -e "${GREEN}🎉 All tests passed!${NC}"
}

stop_container() {
    echo -e "${YELLOW}Stopping container...${NC}"
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    echo -e "${GREEN}✓ Container stopped${NC}"
}

clean_up() {
    echo -e "${YELLOW}Cleaning up...${NC}"
    stop_container
    docker rmi $IMAGE_NAME 2>/dev/null || true
    echo -e "${GREEN}✓ Clean up completed${NC}"
}

show_logs() {
    echo -e "${YELLOW}Showing container logs...${NC}"
    docker logs $CONTAINER_NAME
}

show_usage() {
    echo "Usage: $0 [build|run|test|stop|clean|logs]"
    echo ""
    echo "Commands:"
    echo "  build  - Build Docker image"
    echo "  run    - Run container locally"
    echo "  test   - Test API endpoints"
    echo "  stop   - Stop running container"
    echo "  clean  - Clean up container and image"
    echo "  logs   - Show container logs"
    echo "  all    - Build, run, and test (default)"
}

# Main script
case "${1:-all}" in
    "build")
        build_image
        ;;
    "run")
        run_container
        ;;
    "test")
        test_endpoints
        ;;
    "stop")
        stop_container
        ;;
    "clean")
        clean_up
        ;;
    "logs")
        show_logs
        ;;
    "all")
        build_image
        run_container
        test_endpoints
        ;;
    *)
        show_usage
        exit 1
        ;;
esac