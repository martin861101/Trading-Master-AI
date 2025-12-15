# Trading-Master-AI

 # AI Trading Signal Generator 🏆

Full-stack trading signal generator that uses multiple AI agents to analyze markets and generate trading signals.

## Features

✨ **Multi-Agent Analysis**
- Chart Analyst - Technical patterns and pivots
- Macro Agent - Economic indicators and sentiment
- Market Sentinel - Market flow and volume

📊 **Beautiful UI**
- Glassmorphism design with animated backgrounds
- Real-time confidence scoring
- Agent consensus visualization
- Trade levels (Entry, Stop Loss, Take Profit)

🚀 **Tech Stack**
- **Backend**: FastAPI + Python
- **Frontend**: Vue.js 3 + Vite + Tailwind CSS
- **APIs**: Real-time market data integration

---

## Quick Start

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install fastapi uvicorn python-dotenv

# Start the server
python server.py
```

Backend will run at: `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies  
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

---

## Usage

1. **Start both servers** (backend and frontend)
2. **Open browser** to `http://localhost:5173`
3. **Enter a trading symbol** (e.g., XAUUSD, AAPL, BTCUSD)
4. **Click "Generate Signal"**
5. **Review the AI-generated trading signal**

---

## API Endpoints

### Generate Trading Signal
```
POST /trading/signal
Content-Type: application/json

{
  "symbol": "XAUUSD"
}
```

**Response:**
```json
{
  "asset": "XAUUSD",
  "direction": "LONG|SHORT|HOLD",
  "confidence": 0.75,
  "entry_target": 2650.00,
  "stop_loss_target": 2625.00,
  "take_profit_target": 2700.00,
  "risk_reward_ratio": 2.0,
  "signal_strength": "STRONG|MODERATE|WEAK",
  "agent_consensus": {
    "chartanalyst": "LONG",
    "macroagent": "LONG",
    "marketsentinel": "HOLD"
  },
  "reasoning": "Analysis explanation...",
  "recommendations": ["Wait for confirmation", ...]
}
```

---

## File Structure

```
├── backend/
│   ├── server.py              # FastAPI server
│   ├── state/
│   │   └── graph.py          # Trading signal generator
│   ├── agents/               # Trading advisor agents
│   └── fetchers/             # Market data fetchers
│
└── frontend/
    ├── index.html            # Entry HTML
    ├── src/components/
    │   ├── App.vue          # Main Vue component
    │   ├── main.js          # Vue entry point
    │   └── index.css        # Tailwind styles
    ├── vite.config.js       # Vite configuration
    ├── tailwind.config.js   # Tailwind configuration
    └── package.json         # Frontend dependencies
```

---

## Configuration

### Environment Variables (Optional)

Create `.env` in backend directory:
```
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

---

## Development

### Adding New Agents

1. Create agent file in `backend/agents/`
2. Implement analysis logic
3. Add to `state/graph.py` consensus

### Customizing UI

Edit `frontend/src/components/App.vue`:
- Modify styles in `<style>` section
- Adjust layout in `<template>`
- Add features in `<script>`

---

## Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify Python dependencies installed

**Frontend won't start:**
- Run `npm install` to install dependencies
- Check if port 5173 is available

**No signals generating:**
- Check backend is running at http://localhost:8000
- Open browser console for error messages
- Verify proxy configuration in vite.config.js

---

## Future Enhancements

- [ ] Real-time market data integration
- [ ] Historical backtest visualization
- [ ] Multi-timeframe analysis
- [ ] Alert notifications
- [ ] Portfolio tracking
- [ ] Mobile app version

---

Made with ❤️ for traders by AI


