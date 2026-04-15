"""
HTTP API for the financial analyst agent.

Loads .env before imports that read API keys at import time (e.g. Tavily).
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel, Field  

from main import research_stock  

app = FastAPI(
    title="Financial Analyst Agent",
    description="Run LangGraph financial research for a stock ticker.",
    version="1.0.0",
)


class ResearchRequest(BaseModel):
    ticker: str = Field(
        ...,
        min_length=1,
        max_length=32,
        description="Stock symbol, e.g. AAPL ",
    )


class ResearchResponse(BaseModel):
    ticker: str
    investment_brief: str


@app.get("/")
def root() -> dict[str, str]:
    """So browser or probes hitting the server root get 200 instead of 404."""
    return {
        "service": "financial-analyst-agent",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "research_get": "/v1/research/{ticker}",
        "research_post": "/v1/research",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/research", response_model=ResearchResponse)
def research_post(body: ResearchRequest) -> ResearchResponse:
    ticker = body.ticker.strip()
    if not ticker:
        raise HTTPException(status_code=400, detail="ticker is required")
    try:
        brief = research_stock(ticker, stream=False)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e
    return ResearchResponse(
        ticker=ticker.upper(),
        investment_brief=brief or "",
    )


@app.get("/v1/research/{ticker}", response_model=ResearchResponse)
def research_get(ticker: str) -> ResearchResponse:
    t = ticker.strip()
    if not t:
        raise HTTPException(status_code=400, detail="ticker is required")
    try:
        brief = research_stock(t, stream=False)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e
    return ResearchResponse(
        ticker=t.upper(),
        investment_brief=brief or "",
    )
