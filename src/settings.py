import logging
import sys
import os
from pathlib import Path

from rich.logging import RichHandler
from dotenv import load_dotenv

# sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv(override=True)

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True, tracebacks_suppress=[])],
)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


class ApiKeys:
    PINECONE_INDEX = os.environ.get("PINECONE_INDEX", "")
    PINECONE_ENV = os.environ.get("PINECONE_ENV", "")
    PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
    NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")


class ProjectPaths:
    ROOT_PATH = str(Path(__file__).parent.parent)

    DATA_PATH = os.path.join(ROOT_PATH, "../data")
    EXTERNAL_DATA = os.path.join(DATA_PATH, "external")
    INTERIM_DATA = os.path.join(DATA_PATH, "interim")
    PROCESSED_DATA = os.path.join(DATA_PATH, "processed")
    RAW_DATA = os.path.join(DATA_PATH, "raw")
    EVALUATION_DATA = os.path.join(DATA_PATH, "evaluation")

    MODEL_DATA = os.path.join(ROOT_PATH, "../models")
