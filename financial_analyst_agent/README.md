# Financial Analyst Agent

A ReAct agent powered by NVIDIA NIM and LangGraph that produces a comprehensive investment brief for any stock ticker.

---

## Prerequisites

- Python 3.12
- [`uv`](https://github.com/astral-sh/uv) package manager
- An [NVIDIA API key](https://build.nvidia.com/) (`NVIDIA_API_KEY`)
- A [Tavily API key](https://tavily.com/) (`TAVILY_API_KEY`)

---

## Step 1 — Add your API keys (hidden input)

```bash
cd financial_analyst_agent

read -s -p "NVIDIA_API_KEY: " NVIDIA_KEY && echo
read -s -p "TAVILY_API_KEY: " TAVILY_KEY && echo

echo "NVIDIA_API_KEY=$NVIDIA_KEY" > .env
echo "TAVILY_API_KEY=$TAVILY_KEY" >> .env
```

---

## Step 2 — Set up environment

```bash
uv venv --python 3.12 --seed pyagents
source pyagents/bin/activate
uv pip install -r requirements.txt
```

---

## Step 3 — Run as a service

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

The service starts at `http://localhost:8000` and stays running until you hit `Ctrl+C`.

---

## Step 4 — Query any stock

From any terminal or browser while the service is running:

```bash
# Check the service is healthy
curl http://localhost:8000/health

# Research any stock
curl http://localhost:8000/v1/research/NVDA
curl http://localhost:8000/v1/research/AAPL
curl http://localhost:8000/v1/research/TSLA
curl http://localhost:8000/v1/research/MSFT

```

Or open directly in your browser:
```
http://localhost:8000/v1/research/NVDA
```

Interactive API docs available at:
```
http://localhost:8000/docs
```

---

## Docker (alternative)

Build and run the service in a container:

```bash
read -s -p "NVIDIA_API_KEY: " NVIDIA_KEY && echo
read -s -p "TAVILY_API_KEY: " TAVILY_KEY && echo

docker build -t fa-agent .

docker run --rm -p 8000:8000 \
  -e NVIDIA_API_KEY="$NVIDIA_KEY" \
  -e TAVILY_API_KEY="$TAVILY_KEY" \
  fa-agent
```

Then query exactly the same way as above.

---

## Quick test (single ticker, no server)

```bash
python main.py AAPL
```

Runs the full research loop and prints the investment brief to the terminal.
