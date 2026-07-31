import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

import { getCategoryRevenue } from "../services/dashboardService";

function DemandChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchCategoryRevenue();
  }, []);

  const fetchCategoryRevenue = async () => {
    try {
      const response = await getCategoryRevenue();

      const formattedData = response.map((item) => ({
        category: item.category,
        revenue: item.revenue,
      }));

      setData(formattedData);
    } catch (error) {
      console.error("Error fetching category revenue:", error);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-md p-6">
      <h2 className="text-xl font-bold mb-4">
        Revenue by Category
      </h2>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="category" />

          <YAxis />

          <Tooltip />

          <Bar
            dataKey="revenue"
            fill="#2563eb"
            radius={[6, 6, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DemandChart;