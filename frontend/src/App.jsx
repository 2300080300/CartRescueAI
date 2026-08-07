import { useState } from "react";
import CartForm from "./components/CartForm";
import PredictionChart from "./components/PredictionChart";
import axios from "axios";

const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

function App() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (payload) => {
    setError(null);
    setLoading(true);

    try {
      const response = await axios.post(`${apiBase}/predict`, payload);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-5xl px-4 py-10">
        <header className="mb-10 text-center">
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">
            Cart Rescue AI
          </p>
          <h1 className="mt-4 text-4xl font-semibold text-white">
            Predict cart abandonment and recover lost checkout revenue
          </h1>
          <p className="mt-3 text-slate-300">
            Enter cart behavior details and get a probability score with action recommendations.
          </p>
        </header>

        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <section className="rounded-3xl bg-slate-900/80 p-8 shadow-xl shadow-slate-950/20">
            <CartForm onSubmit={handleSubmit} loading={loading} />
            {error && <p className="mt-4 rounded-xl bg-rose-500/15 p-4 text-rose-200">{error}</p>}
            {prediction && (
              <div className="mt-6 rounded-3xl border border-cyan-500/20 bg-slate-950/90 p-6">
                <h2 className="text-xl font-semibold text-white">Prediction</h2>
                <p className="mt-2 text-slate-300">Abandonment probability: <strong>{(prediction.abandonment_probability * 100).toFixed(1)}%</strong></p>
                <p className="mt-2 text-cyan-200">Recommendation: {prediction.recommendation}</p>
              </div>
            )}
          </section>

          <section className="rounded-3xl bg-slate-900/80 p-8 shadow-xl shadow-slate-950/20">
            <h2 className="text-xl font-semibold text-white">Insights</h2>
            <p className="mt-3 text-slate-400">
              The chart below visualizes the probability of abandonment for your latest prediction.
            </p>
            <PredictionChart prediction={prediction} />
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;
