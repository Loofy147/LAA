
# Stage 1: Build the Rust core library
FROM rust:latest as builder

WORKDIR /app

# Copy only the necessary files to build the Rust library
COPY laa_core /app/laa_core
RUN cd laa_core && cargo build --release

# Stage 2: Build the Python application
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libgtk-4-1 \
    libgraphene-1.0-0 \
    libxslt1.1 \
    libwoff1 \
    libvpx9 \
    libevent-2.1-7 \
    libopus0 \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    flite \
    libwebpdemux2 \
    libavif16 \
    libharfbuzz-icu0 \
    libwebp7 \
    libenchant-2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    x264 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright && playwright install

# Copy the built Rust library from the builder stage
COPY --from=builder /app/laa_core/target/release/liblaa_core.so /app/laa_core.so

# Copy the application code
COPY app.py .

# Expose the port Gradio runs on
EXPOSE 7860

# Run the Gradio app
CMD ["gradio", "app.py", "--server_name", "0.0.0.0"]
