# Cart Rescue AI

Cart Rescue AI is a full-stack web application for predicting cart abandonment and providing insights to recover lost sales.

## Tech Stack

- React + Vite frontend
- FastAPI backend
- PostgreSQL database
- Python 3.12
- Scikit-learn
- XGBoost
- SQLAlchemy
- Tailwind CSS
- Chart.js

## Project Structure

- `backend/` - FastAPI application and model services
- `frontend/` - React + Vite user interface
- `.env.example` - sample environment variables
- `requirements.txt` - Python dependencies

## Setup

### 1. Clone repository

```bash
git clone <repo-url> CartRescueAI
cd CartRescueAI
```

### 2. Python environment

```bash
python -m venv .venv
```

Activate the environment:

- Windows PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Windows CMD:
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

### 3. Frontend dependencies

```bash
cd frontend
npm install
```

### 4. Configure environment

Copy `.env.example` to `.env` and update values.

### 5. Run services

Start the backend from the project root:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Start the frontend:

```bash
cd frontend
npm run dev -- --host
```

### 6. Open the app

Visit `http://localhost:5173` in your browser.

## Notes

- Use PostgreSQL as configured in `.env`.
- The backend includes a sample XGBoost prediction service and a lightweight cart event model.
- Tailwind CSS is configured for production-ready styling.
