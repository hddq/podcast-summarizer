# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# git, make, g++: for building whisper.cpp
# ffmpeg: for audio conversion
# curl: for downloading models (optional, but useful)
RUN apt-get update && apt-get install -y \
    git \
    make \
    cmake \
    g++ \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clone and build whisper.cpp
# We clone into /app/whisper.cpp
RUN git clone https://github.com/ggerganov/whisper.cpp.git /app/whisper.cpp && \
    cd /app/whisper.cpp && \
    cmake -B build && \
    cmake --build build --config Release

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create directories for data persistence
# models: to store ggml models
RUN mkdir -p data/downloads data/transcripts data/models data/summaries

# Run the application
CMD ["python", "main.py"]