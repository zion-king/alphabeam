# Load .env file using:
from dotenv import load_dotenv
load_dotenv(".env")
import os


Env = os.getenv("PYTHON_ENV")
metric_flow_path = os.getenv("METRIC_FLOW_PATH")
semantic_model_path = os.getenv("SEMANTIC_MODEL_PATH")
port = os.getenv("PORT")
llm_model = os.getenv("LLM_MODEL")
google_key = os.getenv("GOOGLE_API_KEY")
chroma_db_host = os.getenv("CHROMADB_HOST")
chroma_db_port = os.getenv("CHROMADB_PORT")
cohere_rerank_key = os.getenv("COHERE_RERANK_KEY")