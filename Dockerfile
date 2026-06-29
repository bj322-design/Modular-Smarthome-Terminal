# Use a lightweight official Python image
FROM python:3.13-slim

# Install system dependencies if required (like build tools for certain wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install UV globally inside the container
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin/:${PATH}"

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definition files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Synchronize dependencies using UV
RUN uv sync --frozen

# Copy the rest of the application files into the container
COPY . .

# Expose the Flask port internally
EXPOSE 5000

# Run the master start script through UV to keep the SQL & plugin threads alive
CMD ["uv", "run", "python", "start.py"]