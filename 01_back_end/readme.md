# Running the Application

## 🐍 Local Development (Python)

1. **Install Dependencies**:

   ```bash
   pip install uv
   uv sync
   ```

2. **Set Up Environment**:
   Create a `.env` file with your API keys:

   ```env
   GOOGLE_API_KEY=your_google_api_key
   MODEL_NAME=your_model_name
   TAVILY_API_KEY=your_tavily_api_key
   CONTEXT7_API_KEY=your_context7_api_key
   ```

3. **Run the Application**:

   ```bash
   python main.py
   ```

   The application will be available at:

   - http://localhost:8000

## 🐳 Docker Development

1. **Build the Docker Image**:

   ```bash
   docker build -t deep-research-assistant .
   ```

2. **Run with Docker**:

   ```bash
   docker run -p 8080:8000 deep-research-assistant
   ```

   Access the application at: 

   - http://localhost:8000

## ☁️ Cloud Deployment (Google Cloud Run)

The project includes a comprehensive Makefile for easy deployment to Google Cloud Run.

### Prerequisites

- Google Cloud CLI installed and configured
- A Google Cloud Project with billing enabled

### Quick Setup and Deployment

1. **Configure the Makefile**:
   Edit the variables at the top of the `Makefile`:

   ```makefile
   PROJECT_ID = your-gcp-project-id
   EMAIL = your-email@domain.com
   ARTIFACT_REGISTRY_REPO = deep-research-repo
   SERVICE_NAME = deep-research-assistant
   SERVICE_ACCOUNT_NAME = deep-research-sa
   ```

2. **Initial Setup**:

   ```bash
   # Authenticate and set up all required services
   make auth
   make setup-full
   ```

3. **Deploy to Cloud Run**:
   ```bash
   # Build, push, and deploy in one command
   make deploy-full
   ```

### Available Make Commands

**Setup Commands**:

- `make auth` - Authenticate to Google Cloud
- `make setup-full` - Complete setup

**Deployment Commands**:

- `make build` - Build Docker image
- `make push` - Push image to artifact registry
- `make deploy` - Deploy to Cloud Run
- `make deploy-full` - Build, push, and deploy (complete pipeline)

