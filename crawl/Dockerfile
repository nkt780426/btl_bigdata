# Stage 1: Build environment
FROM python:3.10-slim as builder

# Set working directory in the image
WORKDIR /app

# Copy only the necessary files from the host file system to the image file system
COPY . /app

# Install the necessary packages
RUN pip install --no-cache-dir Scrapy pykafka itemadapter

# Expose the port
EXPOSE 8000

# Specify the entry point and default command for the runtime
ENTRYPOINT ["scrapy"]

# Start crawl
CMD ["crawl", "kafka"]