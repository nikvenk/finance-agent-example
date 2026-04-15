### For testing locally:

Create a .env file with:

```bash
NVIDIA_API_KEY=xxx
TAVILY_API_KEY=xxx
```

Set up environment:

```bash
uv venv --python 3.12 --seed pyagents
source pyagents/bin/activate
uv pip install -r requirements.txt
```

then run:

```bash
python main.py AAPL
```

### To build docker container:

```bash
export NVIDIA_API_KEY=xxx
export TAVILY_API_KEY=xxx

docker build -t fa-agent .


docker run --rm -p 8000:8000 \
  -e NVIDIA_API_KEY="$NVIDIA_API_KEY" \
  -e TAVILY_API_KEY="$TAVILY_API_KEY" \
  fa-agent:latest
```

### Test endpoint

```bash

curl -s http://localhost:8000/health

curl -s http://localhost:8000/v1/research/AAPL

curl -s -X POST http://localhost:8000/v1/research \
  -H 'Content-Type: application/json' \
  -d '{"ticker":"AAPL"}'

```

