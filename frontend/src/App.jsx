import { useState } from "react";
import CartForm from "./components/CartForm";
import PredictionChart from "./components/PredictionChart";
import Header from "./components/Header";
import DashboardCards from "./components/DashboardCards";
import PredictionResult from "./components/PredictionResult";
import HistoryTable from "./components/HistoryTable";
import axios from "axios";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import StoreNavbar from "./components/StoreNavbar";
import Home from "./pages/Home";
import Products from "./pages/Products";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import CartProvider from "./context/CartContext";
import ShoppingSessionProvider from "./context/ShoppingSessionContext";

const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

function AdminDashboard() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [cart, setCart] = useState(null);

  const handleSubmit = async (payload) => {
    setError(null);
    setLoading(true);

    try {
      const response = await axios.post(`${apiBase}/predict`, payload);
      setPrediction(response.data);
      setCart(payload);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Header />
      <main className="mx-auto max-w-7xl space-y-8 px-4 py-8 sm:px-8">
        <DashboardCards />
        <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
          <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-xl shadow-slate-950/20 sm:p-6"><div className="mb-6"><p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">New assessment</p><h2 className="mt-1 text-xl font-semibold text-white">Analyze a cart session</h2><p className="mt-2 text-sm text-slate-500">Use customer behavior signals to predict abandonment risk.</p></div><CartForm onSubmit={handleSubmit} loading={loading} />{error && <p className="mt-4 rounded-xl border border-rose-400/20 bg-rose-500/10 p-4 text-sm text-rose-200">{error}</p>}</section>
          <div className="space-y-6"><PredictionResult prediction={prediction} cart={cart} /><section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-xl shadow-slate-950/20 sm:p-6"><div className="mb-2"><h2 className="font-semibold text-white">Risk distribution</h2><p className="mt-1 text-sm text-slate-500">Abandonment probability for the latest assessment.</p></div><PredictionChart prediction={prediction} /></section></div>
        </div>
        <HistoryTable />
      </main>
    </div>
  );
}

function Storefront() {
  return <div className="min-h-screen bg-slate-950 text-slate-100"><StoreNavbar /><main className="mx-auto max-w-7xl px-4 py-8 sm:px-8"><Routes><Route path="/" element={<Home />} /><Route path="/products" element={<Products />} /><Route path="/cart" element={<Cart />} /><Route path="/checkout" element={<Checkout />} /></Routes></main></div>;
}

function App() {
  return <CartProvider><ShoppingSessionProvider><BrowserRouter><Routes><Route path="/dashboard" element={<AdminDashboard />} /><Route path="*" element={<Storefront />} /></Routes></BrowserRouter></ShoppingSessionProvider></CartProvider>;
}

export default App;
