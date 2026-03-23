# Local Execution Plan: LLM Twin

Here is the step-by-step structured plan to run the LLM Twin code on your local machine and generate the output locally.

## Prerequisite Checks
1. **Docker**: Ensure Docker is installed (≥v27.1.1) and running. This is used to host your local infrastructure (MongoDB, Qdrant, and ZenML server).
2. **Python Environment**: Ensure Python 3.11 is installed. The book recommends using `pyenv` for managing Python versions.
3. **Poetry**: Ensure Poetry (>= 1.8.3) is installed for dependency management.

## Step 1: Clone and Set Up Environment
1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/PacktPublishing/LLM-Engineers-Handbook.git
   cd LLM-Engineers-Handbook 
   ```
2. **Install local dependencies**: Install dependencies without the heavy AWS specifics, since we are running locally:
   ```bash
   poetry env use 3.11
   poetry install --without aws
   poetry run pre-commit install
   ```
3. **Activate Environment**:
   ```bash
   poetry shell
   ```
   *Explanation:* The project uses **Poe the Poet** (`poetry poe ...`) as a task manager to execute the complex pipeline scripts seamlessly.

## Step 2: Configure Environment Variables
You need to provide your API keys to the system for data collection, experiment tracking, and LLM access.
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open [.env] and fill out the mandatory local variables:
   - `OPENAI_API_KEY`: Required for data generation and RAG pipelines.
   - `HUGGINGFACE_ACCESS_TOKEN`: Required to download/upload models.
   - `COMET_API_KEY`: Required for experiment tracking (Comet ML) and prompt monitoring (Opik).

## Step 3: Spin Up Local Infrastructure
The LLM architecture relies on several local databases and orchestrators. Bring them up using Docker:
```bash
poetry poe local-infrastructure-up
```
*Outputs generated locally:*
- **ZenML** (Orchestrator): Runs at `localhost:8237`. Coordinates data processing and MLOps workflows.
- **Qdrant** (Vector Database): Runs at `localhost:6333`. Used for storing embeddings and vector search in the RAG pipeline.
- **MongoDB** (NoSQL Data Warehouse): Runs on port `27017`. Used to store unstructured raw scraped data.

## Step 4: Run Data Engineering & Processing Pipelines
Now you will execute the ZenML pipelines locally to gather and format the data.
1. **Data Collection ETL**:
   ```bash
   poetry poe run-digital-data-etl
   ```
   *Output*: Crawls GitHub, Medium, etc., and stores the raw text in the local MongoDB. (Note: Requires a Chromium-browser/Selenium).
2. **Feature Engineering**:
   ```bash
   poetry poe run-feature-engineering-pipeline
   ```
   *Output*: Cleans the data, chunks it, embeds it, and saves the vectors to the local Qdrant database.
3. **Generate Datasets** (Instruct & Preference):
   ```bash
   poetry poe run-generate-instruct-datasets-pipeline
   poetry poe run-generate-preference-datasets-pipeline
   ```
   *Output*: Uses the OpenAI API to generate instruction and preference datasets used for fine-tuning.

## Step 5: Generating Inference Outputs Locally
> [!WARNING]
> While data generation and vector deployments are run locally, training the LLM (SFT/DPO) and running the real-time LLM inference microservice requires heavy GPU compute. The book offloads these specific tasks to **AWS SageMaker**. However, you can still test the RAG context retrieval locally.

1. **Test the RAG Retrieval Module**:
   To query your local Qdrant database and see the RAG retrieval output without needing the full SageMaker LLM endpoint:
   ```bash
   poetry poe call-rag-retrieval-module
   ```
   *Output*: It queries the Qdrant DB, applies advanced pre-retrieval (query expansion) and post-retrieval (reranking), and outputs the retrieved context to your terminal.

2. **Utility Data Exports**:
   You can export your gathered data and artifacts locally into JSON format to manually inspect what was generated:
   ```bash
   poetry poe run-export-data-warehouse-to-json
   poetry poe run-export-artifact-to-json-pipeline
   ```

## Tear Down
Once finished, safely spin down the local Docker infrastructure to free up memory:
```bash
poetry poe local-infrastructure-down
```
