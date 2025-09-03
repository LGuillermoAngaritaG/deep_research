FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files first (for better caching)
COPY pyproject.toml ./

# Install dependencies with uv (system-wide, no venv)
RUN uv pip install -r pyproject.toml --system

# Copy application files
COPY . .

# Run the application
CMD ["python", "main.py"]