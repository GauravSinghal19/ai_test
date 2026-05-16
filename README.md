# AI Chat Agent Monorepo

This project is a monorepo containing a Python-based AI agent backend and a Next.js frontend chat interface.

## Architecture

- **`/agents`**: Backend application built with Python and the [Google Agent Development Kit (ADK)](https://github.com/google/adk-python).
  - Uses `uv` for package management.
  - Features a multi-agent hierarchy with a root Coordinator agent and specialized sub-agents.
- **`/app`**: Frontend web application built with Next.js, React, and TypeScript.
  - Uses `npm` for package management.
  - Provides a modern chat UI for interacting with the AI agents.

## Prerequisites

- [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/docs/install)
- [Python 3.10+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)
- [Node.js 18+](https://nodejs.org/)
- [npm](https://www.npmjs.com/)

## Authentication

This project uses Google Cloud Application Default Credentials (ADC). You do **not** need to provide an API key in a `.env` file.

1.  Ensure you have a Google Cloud project with the **Vertex AI API** enabled.
2.  Authenticate your local environment:
    ```bash
    gcloud auth application-default login
    ```
3.  Set your Google Cloud project ID (if not already set):
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

## Getting Started

### 1. Install Dependencies

From the root directory, run:
```bash
npm install
```
This will install root dependencies and trigger installations in both `/app` and `/agents`.

### 2. Run the Application

Start both the frontend and backend simultaneously:
```bash
npm run dev
```

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)

## Agent Hierarchy

The backend implements a hierarchical agent structure:
- **Coordinator**: The root agent that receives all user input.
- **Calculator**: A specialized sub-agent for mathematical operations.
- **Weather**: A specialized sub-agent for weather-related queries.

The Coordinator will automatically delegate tasks to the appropriate sub-agent based on the user's request.
