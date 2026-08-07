import { useEffect, useRef } from "react";
import { Chart as ChartJS, registerables } from "chart.js";

ChartJS.register(...registerables);

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

    chartRef.current = new ChartJS(context, {
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
        maintainAspectRatio: false,
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
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [prediction]);

  return (
    <div className="mt-6">
      <h3 className="mb-4 text-lg font-semibold text-white">
        Current Score
      </h3>

      {!prediction && (
        <p className="mb-4 text-slate-400">
          Submit a cart scenario to view the score.
        </p>
      )}

      <div style={{ height: "300px" }}>
        <canvas ref={canvasRef}></canvas>
      </div>
    </div>
  );
}