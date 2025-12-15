from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
import os
import traceback
from dotenv import load_dotenv

# =========================
# ENV
# =========================
load_dotenv()

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="MCP Trading & Research API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# MODELS
# =========================
class TradingSignalRequest(BaseModel):
    symbol: str


class LearningSummaryRequest(BaseModel):
    mode: str
    topic: str = ""
    url: str = ""
    email: str = ""


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
async def health():
    return {"status": "ok"}


# =========================
# SAFE TRADING SIGNAL ENDPOINT
# =========================
@app.post("/trading/signal")
async def generate_trading_signal(request: TradingSignalRequest):
    """
    SAFE MODE:
    - Will NEVER crash
    - Falls back to HOLD if TradingGraph fails
    """

    symbol = request.symbol.upper()

    try:
        # ---- Use REAL Gold Orchestrator ----
        print(f"\n{'='*60}")
        print(f"🎯 TRADING SIGNAL REQUEST: {symbol}")
        print(f"{'='*60}\n")
        
        try:
            import sys
            import os
            
            print("📂 Setting up paths...")
            # Add agents and fetchers directories to path
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            agents_dir = os.path.join(backend_dir, "agents")
            fetchers_dir = os.path.join(backend_dir, "fetchers")
            
            print(f"   Backend dir: {backend_dir}")
            print(f"   Agents dir: {agents_dir}")
            print(f"   Fetchers dir: {fetchers_dir}")
            
            if agents_dir not in sys.path:
                sys.path.insert(0, agents_dir)
                print(f"   ✓ Added agents to path")
            if fetchers_dir not in sys.path:
                sys.path.insert(0, fetchers_dir)
                print(f"   ✓ Added fetchers to path")
            
            print("\n📦 Importing gold orchestrator...")
            from agents.gold_orchestrator import run_gold_orchestration
            print("   ✓ Import successful!\n")
            
            print(f"🔄 Generating LIVE signal for {symbol}...")
            print("-" * 60)
            
            # Run the real orchestration
            result = await run_gold_orchestration(
                timeframe="1h",
                verbose=True,
                save_json=False
            )
            
            print("-" * 60)
            print(f"✅ Orchestration completed!")
            print(f"   Signal: {result.get('signal', {}).get('direction', 'UNKNOWN')}")
            print(f"   Confidence: {result.get('signal', {}).get('confidence', 0):.1%}\n")
            
            # Transform the orchestrator output to API format
            if result and result.get("signal"):
                sig = result["signal"]
                agent_consensus = result.get("agent_consensus", {})
                
                return {
                    "asset": result.get("symbol", symbol),
                    "direction": sig.get("direction", "HOLD"),
                    "confidence": float(sig.get("confidence", 0.0)),
                    "entry_target": float(result.get("trade_levels", {}).get("entry", 0.0)),
                    "stop_loss_target": float(result.get("trade_levels", {}).get("stop_loss", 0.0)),
                    "take_profit_target": float(result.get("trade_levels", {}).get("take_profit", 0.0)),
                    "risk_reward_ratio": float(result.get("trade_levels", {}).get("risk_reward", 0.0)),
                    "signal_strength": sig.get("strength", "WEAK"),
                    "agent_consensus": agent_consensus,
                    "reasoning": result.get("reasoning", ""),
                    "recommendations": result.get("recommendations", []),
                    "next_review_time": result.get("next_review", "1h"),
                }

        except Exception as e:
            print(f"\n❌ REAL ORCHESTRATOR ERROR: {e}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            print("   ⚠️  FALLING BACK TO SAFE MODE\n")

        # ---- SAFE FALLBACK RESPONSE ----
        return {
            "asset": symbol,
            "direction": "HOLD",
            "confidence": 0.50,
            "entry_target": 0.0,
            "stop_loss_target": 0.0,
            "take_profit_target": 0.0,
            "risk_reward_ratio": 0.0,
            "signal_strength": "WEAK",
            "agent_consensus": {
                "chartanalyst": "HOLD",
                "macroagent": "HOLD",
                "marketsentinel": "HOLD",
            },
            "reasoning": "Trading engine unavailable — safe fallback used.",
            "recommendations": [
                "Wait for confirmation",
                "Reduce position size",
                "Check higher timeframe trend",
            ],
            "next_review_time": "1h",
        }

    except Exception as e:
        # Absolute last-resort protection
        print("\n--- FATAL ERROR ---")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Fatal trading endpoint error")


# =========================
# RESEARCH ENDPOINT
# =========================
@app.post("/learning_summary")
async def generate_learning_summary(request: LearningSummaryRequest):
    """
    Generate learning summary for topic or URL.
    """

    mode = request.mode
    topic = request.topic
    url = request.url
    email = request.email

    try:
        # Mock summary for now
        if mode == "topic":
            summary = f"Comprehensive learning summary for '{topic}':\n\nKey concepts:\n- Concept 1\n- Concept 2\n\nResources:\n- Resource 1\n- Resource 2\n\nLearning path:\n1. Step 1\n2. Step 2"
        elif mode == "url":
            summary = f"Summary of content from {url}:\n\nMain points:\n- Point 1\n- Point 2\n\nKey takeaways:\n- Takeaway 1\n- Takeaway 2"
        else:
            summary = "Invalid mode. Use 'topic' or 'url'."

        return {"summary": summary}

    except Exception as e:
        print(f"Error generating summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate summary")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
