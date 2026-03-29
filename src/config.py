"""
Configuration — Load environment variables and expose shared settings.

Usage:
    from src.config import llm, OPENAI_MODEL
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env from project root
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-your-key-here":
    raise ValueError(
        "OPENAI_API_KEY is not set. "
        "Please add a valid key to your .env file."
    )

# Shared LLM instance used by all agents
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0.3,          # Low temp for factual tasks
    openai_api_key=OPENAI_API_KEY,
)
