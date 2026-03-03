#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Default to current directory if no argument is provided
TARGET_DIR="${1:-.}"

echo "Searching for __pycache__ directories in: $TARGET_DIR"

# Find and remove all __pycache__ directories
find "$TARGET_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} +

echo "All __pycache__ directories removed."