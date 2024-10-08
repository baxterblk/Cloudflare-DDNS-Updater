#!/bin/bash

# Exit on any error
set -e

echo "Starting project reorganization..."

# Create necessary directories
mkdir -p templates static data
echo "Created directories: templates, static, data (if they didn't exist)"

# Move files from Docker directory to root
if [ -d "Docker" ]; then
    echo "Moving files from Docker directory to root..."
    mv Docker/Dockerfile ./ 2>/dev/null || echo "Dockerfile already in root"
    mv Docker/app.py ./ 2>/dev/null || echo "app.py already in root"
    mv Docker/ddns_updater.py ./ 2>/dev/null || echo "ddns_updater.py already in root"
    mv Docker/requirements.txt ./ 2>/dev/null || echo "requirements.txt already in root"
    
    # Move template files
    if [ -d "Docker/templates" ]; then
        mv Docker/templates/* templates/ 2>/dev/null || echo "Template files already moved"
    else
        echo "No templates directory found in Docker folder"
    fi

    # Remove Docker directory if it's empty
    if [ -z "$(ls -A Docker)" ]; then
        rm -rf Docker
        echo "Removed empty Docker directory"
    else
        echo "Docker directory not empty, please check its contents manually"
    fi
else
    echo "No Docker directory found, skipping file moves"
fi

# Check docker-compose.yml
if [ -f "Docker/docker-compose.yml" ] && [ -f "docker-compose.yml" ]; then
    echo "docker-compose.yml exists in both root and Docker directory. Please compare them manually."
elif [ -f "Docker/docker-compose.yml" ]; then
    mv Docker/docker-compose.yml ./
    echo "Moved docker-compose.yml from Docker directory to root"
elif [ -f "docker-compose.yml" ]; then
    echo "docker-compose.yml already in root directory"
else
    echo "No docker-compose.yml found"
fi

echo "Reorganization complete. New directory structure:"
tree -L 2

echo "Please review the changes and ensure all files are in the correct locations."
