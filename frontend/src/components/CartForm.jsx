import { useState } from "react";

const initialValues = {
  session_duration: 2.5,
  items_in_cart: 1,
  total_value: 79.99,
  device_type: "desktop",
  source: "organic",
};

export default function CartForm({ onSubmit, loading }) {
  const [values, setValues] = useState(initialValues);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setValues((current) => ({
      ...current,
      [name]: name === "items_in_cart" ? parseInt(value, 10) : name === "session_duration" || name === "total_value" ? parseFloat(value) : value,
    }));
  };

  const submit = (event) => {
    event.preventDefault();
    onSubmit(values);
  };

  return (
    <form onSubmit={submit} className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="text-sm text-slate-300">Session duration (minutes)</span>
          <input
            name="session_duration"
            value={values.session_duration}
            onChange={handleChange}
            type="number"
            step="0.1"
            min="0"
            className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400"
          />
        </label>

        <label className="block">
          <span className="text-sm text-slate-300">Items in cart</span>
          <input
            name="items_in_cart"
            value={values.items_in_cart}
            onChange={handleChange}
            type="number"
            min="0"
            className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400"
          />
        </label>
      </div>

      <label className="block">
        <span className="text-sm text-slate-300">Cart total value</span>
        <input
          name="total_value"
          value={values.total_value}
          onChange={handleChange}
          type="number"
          step="0.01"
          min="0"
          className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400"
        />
      </label>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="text-sm text-slate-300">Device type</span>
          <select
            name="device_type"
            value={values.device_type}
            onChange={handleChange}
            className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400"
          >
            <option value="desktop">Desktop</option>
            <option value="mobile">Mobile</option>
            <option value="tablet">Tablet</option>
          </select>
        </label>

        <label className="block">
          <span className="text-sm text-slate-300">Traffic source</span>
          <select
            name="source"
            value={values.source}
            onChange={handleChange}
            className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400"
          >
            <option value="organic">Organic</option>
            <option value="email">Email</option>
            <option value="social">Social</option>
            <option value="campaign">Campaign</option>
          </select>
        </label>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="inline-flex w-full items-center justify-center rounded-3xl bg-cyan-500 px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:bg-slate-700"
      >
        {loading ? "Analyzing..." : "Predict abandonment"}
      </button>
    </form>
  );
}
