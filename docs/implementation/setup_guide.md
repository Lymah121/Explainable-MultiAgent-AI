# Setup Guide

> How to set up the development environment and run the project.

---

## Prerequisites

- Python 3.10+
- OpenAI API key
- Git

## Environment Setup

```bash
# Clone the repository
git clone https://github.com/Lymah121/Explainable-MultiAgent-AI.git
cd Explainable-MultiAgent-AI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## API Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
```

> ⚠️ Never commit `.env` to git — it's already in `.gitignore`.

## Required Packages

```
langgraph
langchain
langchain-openai
python-dotenv
pydantic
```

## Running the Project

```bash
# Run the full pipeline (coming soon)
python src/main.py --task "Summarize and fact-check this article"

# Run individual agents for testing (coming soon)
python src/agents/researcher.py --test
```

## Development Notes

- Use `GPT-3.5-turbo` for development/testing to save costs
- Switch to `GPT-4` for final experimental runs
- Set token budget limits in `.env` to avoid cost surprises
