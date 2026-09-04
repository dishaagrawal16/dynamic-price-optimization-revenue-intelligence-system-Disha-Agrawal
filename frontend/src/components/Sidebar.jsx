import { Link, useNavigate } from "react-router-dom";
import {
  FaChartLine,
  FaBox,
  FaRobot,
  FaChartBar,
  FaChartArea,
  FaStore,
  FaSignOutAlt,
} from "react-icons/fa";

function Sidebar() {
  const navigate = useNavigate();
  const handleLogout = () => {
  localStorage.removeItem("token");
  navigate("/");
};
  return (
    <div className="w-64 h-screen bg-blue-700 text-white fixed left-0 top-0 shadow-lg">

      <div className="text-3xl font-bold p-6 border-b border-blue-500">
        🚀 PricePilot AI
      </div>

      <nav className="mt-6 flex flex-col">

        <Link
          to="/dashboard"
          className="flex items-center gap-3 px-6 py-4 hover:bg-blue-600 transition"
        >
          <FaChartLine />
          Dashboard
        </Link>

        <Link
          to="/products"
          className="flex items-center gap-3 px-6 py-4 hover:bg-blue-600 transition"
        >
          <FaBox />
          Products
        </Link>

        <Link
          to="/prediction"
          className="flex items-center gap-3 px-6 py-4 hover:bg-blue-600 transition"
        >
          <FaRobot />
          Prediction
        </Link>

        <Link
          to="/demand-forecast"
          className="flex items-center gap-3 px-6 py-4 hover:bg-blue-600 transition"
          >
          <FaChartArea />
          Demand Forecast
        </Link>

        <Link
  to="/competitor-analysis"
  className="flex items-center gap-3 px-6 py-4 hover:bg-blue-600 transition"
>
  <FaStore />
  Competitor Analysis
</Link>

        <Link
          to="/analytics"
          className="flex items-center gap-3 px-6 py-4 hover:bg-blue-600 transition"
        >
          <FaChartBar />
          Analytics
        </Link>

        <button
  onClick={handleLogout}
  className="flex items-center gap-3 px-6 py-4 mt-auto hover:bg-red-500 transition text-left w-full"
>
  <FaSignOutAlt />
  Logout
</button>

      </nav>
    </div>
  );
}

export default Sidebar;