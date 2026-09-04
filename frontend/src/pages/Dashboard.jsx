import Layout from "../components/Layout";
import DashboardCard from "../components/DashboardCard";
import RevenueChart from "../components/RevenueChart";
import DemandChart from "../components/DemandChart";
import PaymentChart from "../components/PaymentChart";
import RecentProducts from "../components/dashboard/RecentProducts";
import { useEffect, useState } from "react";
import {
  getDashboardSummary,
  getMonthlyRevenue,
  getCategoryRevenue,
  getPaymentDistribution,
  getRecentProducts,
} from "../services/dashboardService";
import { FaDollarSign, FaBoxOpen, FaChartLine } from "react-icons/fa";

function Dashboard() {
  const [summary, setSummary] = useState({
    total_products: 0,
    total_revenue: 0,
    total_discount: 0,
    average_price: 0,
  });

  const [dashboardData, setDashboardData] = useState({
    monthlyRevenue: [],
    categoryRevenue: [],
    paymentDistribution: [],
    recentProducts: [],
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);

        const [
          summaryData,
          monthlyRevenue,
          categoryRevenue,
          paymentDistribution,
          recentProducts,
        ] = await Promise.all([
          getDashboardSummary(),
          getMonthlyRevenue(),
          getCategoryRevenue(),
          getPaymentDistribution(),
          getRecentProducts(),
        ]);

        setSummary(summaryData);

        setDashboardData({
          monthlyRevenue,
          categoryRevenue,
          paymentDistribution,
          recentProducts,
        });
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <Layout title="Dashboard">
      <h1 className="text-3xl font-bold">
        Welcome to PricePilot AI 🚀
      </h1>

      <p className="text-gray-600 mt-2">
        Dynamic Pricing Optimization & Revenue Intelligence System
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
        <DashboardCard
          title="Revenue"
          value={`₹${Number(summary.total_revenue).toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}`}
          icon={<FaDollarSign />}
          color="text-green-600"
        />

        <DashboardCard
          title="Products"
          value={summary.total_products}
          icon={<FaBoxOpen />}
          color="text-blue-600"
        />

        <DashboardCard
          title="Average Price"
          value={`₹${Number(summary.average_price).toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}`}
          icon={<FaChartLine />}
          color="text-orange-500"
        />

        <DashboardCard
          title="Total Discount"
          value={`₹${Number(summary.total_discount).toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}`}
          icon={<FaChartLine />}
          color="text-red-500"
        />
      </div>

      {loading ? (
        <div className="mt-10 text-center text-gray-500">
          Loading dashboard data...
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-10">
          <RevenueChart data={dashboardData.monthlyRevenue} />
          <DemandChart data={dashboardData.categoryRevenue} />
          <PaymentChart data={dashboardData.paymentDistribution} />
          <RecentProducts data={dashboardData.recentProducts} />
        </div>
      )}
    </Layout>
  );
}

export default Dashboard;