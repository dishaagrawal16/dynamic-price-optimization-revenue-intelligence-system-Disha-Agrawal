import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import Analytics from "./pages/Analytics";
import PricePrediction from "./pages/PricePrediction";
import DemandForecast from "./pages/DemandForecast";
import CompetitorAnalysis from "./pages/CompetitorAnalysis";
function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Authentication */}
        <Route path="/" element={<Login />} />

        <Route path="/register" element={<Register />} />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* Products */}
        <Route
          path="/products"
          element={
            <ProtectedRoute>
              <Products />
            </ProtectedRoute>
          }
        />

        {/* Analytics */}
        <Route
          path="/analytics"
          element={
            <ProtectedRoute>
              <Analytics />
            </ProtectedRoute>
          }
        />

        {/* Price Prediction */}
        <Route
          path="/prediction"
          element={
            <ProtectedRoute>
              <PricePrediction />
            </ProtectedRoute>
          }
        />

        {/* Demand Forecast */}
        <Route
          path="/demand-forecast"
          element={
            <ProtectedRoute>
              <DemandForecast />
            </ProtectedRoute>
          }
        />

        {/* Competitor Analysis */}
        <Route
          path="/competitor-analysis"
          element={
            <ProtectedRoute>
              <CompetitorAnalysis />
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;