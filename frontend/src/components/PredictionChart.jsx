import { useEffect, useRef } from "react";
import { Chart, ArcElement, Tooltip, Legend } from "chart.js";

Chart.register(ArcElement, Tooltip, Legend);

export default function PredictionChart({ prediction }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    const context = canvasRef.current.getContext("2d");

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const score = prediction ? prediction.abandonment_probability : 0;
    chartRef.current = new Chart(context, {
      type: "doughnut",
      data: {
        labels: ["Abandonment", "Retention"],
        datasets: [
          {
            data: [score * 100, 100 - score * 100],
            backgroundColor: ["#22d3ee", "#334155"],
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: {
              color: "#cbd5e1",
            },
          },
        },
      },
    });

    return () => {
      chartRef.current?.destroy();
    };
  }, [prediction]);

  return (
    <div className="mt-6 rounded-3xl bg-slate-950/80 p-6 text-center">
      <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Current score</p>
      <canvas ref={canvasRef} className="mt-6" />
      {!prediction && <p className="mt-4 text-slate-400">Submit a cart scenario to view the score.</p>}
    </div>
  );
}
